#!/usr/bin/env python3
"""
Coleta polígonos do IBGE e gera GeoJSONs enriquecidos prontos para CDN.

Output:
  dist/estados.geojson
  dist/municipios/{UF}.geojson
  dist/municipios/all.geojson
  dist/municipios-index.json
"""

import gzip
import json
import os
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

DIST = Path(__file__).parent / "dist"
THROTTLE = 0.3  # segundos entre requests

UFS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                raw = r.read()
                if r.info().get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
                return json.loads(raw.decode("utf-8"))
        except Exception as e:
            if attempt < retries - 1:
                print(f"  retry {attempt + 1} ({e})")
                time.sleep(2)
            else:
                raise
    return None


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def pad7(code):
    return str(code).zfill(7)


def build_estados():
    out_path = DIST / "estados.geojson"
    if out_path.exists():
        print("estados.geojson já existe, pulando (use --force para reprocessar)")
        return

    print("Coletando estados...")
    malhas = fetch(
        "https://servicodados.ibge.gov.br/api/v4/malhas/paises/BR"
        "?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=UF"
    )
    time.sleep(THROTTLE)

    localidades = fetch("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    time.sleep(THROTTLE)

    # monta lookup: código numérico → metadados
    meta = {str(e["id"]): e for e in localidades}

    features = []
    for feature in malhas["features"]:
        code = str(feature.get("id", feature.get("properties", {}).get("codarea", "")))
        info = meta.get(code, {})
        sigla = info.get("sigla", "")
        feature["properties"] = {
            "cd_geocuf": code,
            "nome": info.get("nome", ""),
            "sigla": sigla,
            "hc-key": f"br-{sigla.lower()}" if sigla else "",
        }
        features.append(feature)

    save(out_path, {"type": "FeatureCollection", "features": features})
    print(f"  {len(features)} estados salvos")


def build_municipios(uf, force=False):
    out_path = DIST / "municipios" / f"{uf}.geojson"
    if out_path.exists() and not force:
        print(f"  {uf} já existe, pulando")
        return None

    malhas = fetch(
        f"https://servicodados.ibge.gov.br/api/v4/malhas/estados/{uf}"
        "?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio"
    )
    time.sleep(THROTTLE)

    localidades = fetch(
        f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    )
    time.sleep(THROTTLE)

    # lookup: código 7 dígitos → nome
    meta = {pad7(m["id"]): m["nome"] for m in localidades}

    features = []
    for feature in malhas["features"]:
        code_raw = str(feature.get("id", feature.get("properties", {}).get("codarea", "")))
        code = pad7(code_raw)
        nome = meta.get(code, "")
        feature["properties"] = {
            "cd_geocmu": code,
            "nome": nome,
            "uf": uf,
            "hc-key": f"br-{uf.lower()}-{code}",
        }
        features.append(feature)

    fc = {"type": "FeatureCollection", "features": features}
    save(out_path, fc)
    print(f"  {uf}: {len(features)} municípios")
    return features


def build_all_and_index(force=False):
    all_path = DIST / "municipios" / "all.geojson"
    index_path = DIST / "municipios-index.json"

    if all_path.exists() and index_path.exists() and not force:
        print("all.geojson e municipios-index.json já existem, pulando")
        return

    print("Consolidando all.geojson e index...")
    all_features = []
    index = {}

    for uf in UFS:
        uf_path = DIST / "municipios" / f"{uf}.geojson"
        if not uf_path.exists():
            print(f"  AVISO: {uf}.geojson não encontrado, pulando do consolidado")
            continue
        with open(uf_path, encoding="utf-8") as f:
            fc = json.load(f)
        for feature in fc["features"]:
            cd = feature["properties"].get("cd_geocmu")
            if cd:
                index[cd] = len(all_features)
            all_features.append(feature)

    save(all_path, {"type": "FeatureCollection", "features": all_features})
    save(index_path, index)
    print(f"  {len(all_features)} municípios totais, {len(index)} entradas no index")


def main():
    import sys
    force = "--force" in sys.argv

    DIST.mkdir(exist_ok=True)
    (DIST / "municipios").mkdir(exist_ok=True)

    build_estados()

    print("Coletando municípios por UF (paralelo)...")
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(build_municipios, uf, force): uf for uf in UFS}
        for future in as_completed(futures):
            uf = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"  ERRO {uf}: {e}")

    build_all_and_index(force=force)
    print("Pronto.")


if __name__ == "__main__":
    main()
