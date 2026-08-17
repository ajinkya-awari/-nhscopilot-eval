from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from .contracts import PublicBundle


def load_frozen_bundle(path: Path) -> PublicBundle:
    return PublicBundle.model_validate_json(path.read_text(encoding="utf-8"))


def catalogue_rows(bundle: PublicBundle) -> list[dict[str, Any]]:
    return [
        {
            "model": aggregate.model_id,
            "category": aggregate.category,
            "status": aggregate.status,
            **aggregate.metrics,
        }
        for aggregate in bundle.aggregates
    ]


def export_static_catalogue(bundle: PublicBundle, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = catalogue_rows(bundle)
    body = json.dumps(rows, indent=2, sort_keys=True)
    html = (
        "<!doctype html><meta charset='utf-8'>"
        "<title>NHSCopilot-Eval aggregate catalogue</title>"
        "<h1>NHSCopilot-Eval aggregate catalogue</h1>"
        "<p>Research evaluation only; not clinical advice.</p>"
        "<p>Does not establish clinical safety or regulatory compliance.</p>"
        f"<pre>{escape(body)}</pre>"
    )
    path.write_text(html, encoding="utf-8")


def build_gradio_app(bundle: PublicBundle):
    import gradio as gr

    with gr.Blocks() as demo:
        gr.Markdown(
            "# NHSCopilot-Eval aggregate catalogue\n"
            "Research evaluation only; not clinical advice; no live inference."
        )
        gr.JSON(value=catalogue_rows(bundle), label="Frozen aggregate results")
    return demo
