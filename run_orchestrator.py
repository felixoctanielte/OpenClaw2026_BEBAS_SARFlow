import argparse
import json
from pathlib import Path

import yaml

from modules.briefing import build_briefing
from modules.extraction import extract_incident
from modules.intake import build_follow_up_questions
from modules.rag import load_rag_sources, search_rag
from modules.report import build_final_report
from modules.timeline import append_timeline_event, load_timeline


DEFAULT_DEMO_REPORT = (
    "Mas, ada 2 pendaki belum turun dari Pos 3 Gunung Lawu. "
    "Terakhir kontak jam 18.10. Logistik tinggal sedikit, hujan, sinyal putus. "
    "Pelapor teman rombongan, nomor 081234567890."
)


def load_config(path: str = "agent-config.yml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_state(path: str, state: dict) -> None:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def run_once(text: str, command: str = "intake") -> dict:
    cfg = load_config()
    rag_docs = load_rag_sources(cfg["agent"]["rag_sources"])
    sop_context = search_rag(
        rag_docs,
        "persyaratan pelapor kontak lokasi waktu korban verifikasi laporan SAR",
        limit=3,
    )

    incident = extract_incident(text)
    follow_up_questions = build_follow_up_questions(incident, max_questions=cfg["intake"]["max_follow_up_questions"])
    briefing = build_briefing(incident, follow_up_questions, sop_context)
    timeline_event = append_timeline_event(cfg["storage"]["timeline_file"], text, incident)
    save_state(cfg["storage"]["state_file"], incident)
    timeline = load_timeline(cfg["storage"]["timeline_file"])
    report = build_final_report(incident, timeline)

    return {
        "agent": cfg["agent"]["name"],
        "command": command,
        "incident": incident,
        "follow_up_questions": follow_up_questions,
        "briefing": briefing,
        "timeline_event": timeline_event,
        "timeline": timeline,
        "report": report,
    }


def reset_storage() -> None:
    cfg = load_config()
    for key in ["state_file", "timeline_file"]:
        path = Path(cfg["storage"][key])
        if path.exists():
            path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="SARFlow KOM orchestrator")
    parser.add_argument("--text", default="", help="Incoming report text. Uses a demo report when empty.")
    parser.add_argument("--command", default="intake", choices=["intake", "briefing", "timeline", "report", "json"])
    parser.add_argument("--reset", action="store_true", help="Clear local incident state and timeline before running.")
    args = parser.parse_args()

    if args.reset:
        reset_storage()

    text = args.text.strip() or DEFAULT_DEMO_REPORT
    result = run_once(text, args.command)

    if args.command == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "briefing":
        print(result["briefing"])
    elif args.command == "timeline":
        for event in result["timeline"]:
            print(f"[{event['time_local']}] {event['summary']} Status: {event['verification_status']}")
    elif args.command == "report":
        print(result["report"])
    else:
        print(result["briefing"])
        print("\nTIMELINE EVENT")
        print(f"[{result['timeline_event']['time_local']}] {result['timeline_event']['summary']}")


if __name__ == "__main__":
    main()
