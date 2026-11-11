#!/usr/bin/env python3
"""Publica gh-pages en Cloudflare Pages usando API y secretos de GitHub Actions.

No imprime tokens y no utiliza Workers. Requiere permisos Cloudflare Pages: Edit.
Sin credenciales, avisa claramente: el despliegue en Cloudflare NO será automático.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

PROJECT = "elconsaburense"
API = "https://api.cloudflare.com/client/v4"
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()

def request(path: str, *, body: bytes | None = None, content_type: str | None = None) -> dict:
    headers = {"Authorization": "Bearer " + TOKEN, "Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(
        API + path, data=body, headers=headers, method="POST" if body is not None else "GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read(1000).decode("utf-8", errors="replace")
        raise RuntimeError(f"Cloudflare API HTTP {error.code}: {detail}") from error
    if not result.get("success"):
        raise RuntimeError("Cloudflare API error: " + str(result.get("errors", [])))
    return result["result"]

def main() -> None:
    if not TOKEN or not ACCOUNT:
        print("::warning::Faltan CLOUDFLARE_API_TOKEN y/o CLOUDFLARE_ACCOUNT_ID en "
              "GitHub Actions Secrets. La rama gh-pages se ha actualizado, "
              "pero Cloudflare Pages necesita todavía un despliegue manual.")
        return
    sha = subprocess.check_output(
        ["git", "ls-remote", "origin", "refs/heads/gh-pages"],
        text=True, timeout=30
    ).strip().split()[0]
    if len(sha) != 40:
        raise RuntimeError("No se pudo verificar el commit gh-pages publicado")
    print("Publicación gh-pages:", sha[:12])
    boundary = "----ElConsaburenseDeployBranch"
    data = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="branch"\r\n\r\n'
        f"gh-pages\r\n--{boundary}--\r\n"
    ).encode("utf-8")
    base = f"/accounts/{ACCOUNT}/pages/projects/{PROJECT}/deployments"
    deployment = request(base, body=data, content_type=f"multipart/form-data; boundary={boundary}")
    deployment_id = deployment.get("id")
    actual = deployment.get("deployment_trigger", {}).get("metadata", {}).get("commit_hash")
    if actual != sha:
        raise RuntimeError(f"Cloudflare tomó el commit {actual!r} y se esperaba {sha}")
    print("Despliegue Cloudflare solicitado:", deployment_id)
    for _ in range(45):
        state = request(base + "/" + str(deployment_id))
        status = state.get("latest_stage", {}).get("status")
        if status == "success":
            print(f"::notice::Cloudflare Pages producción actualizado: {state.get('url')}")
            return
        if status in ("failure", "failed", "cancelled", "canceled", "error"):
            raise RuntimeError(f"Cloudflare Pages falló con estado {status}")
        time.sleep(5)
    raise RuntimeError("Cloudflare Pages no terminó dentro del tiempo de verificación")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"::error::{error}", file=sys.stderr)
        raise SystemExit(1)
