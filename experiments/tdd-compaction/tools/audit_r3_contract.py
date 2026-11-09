"""Agent-audit check for R3 (read-only): re-run each hidden assertion separately on a copy of every
R3 final tree, to separate the request's input contract ("splits a list") from the unsupported
tuple-input assertion in `test_returns_lists`. Writes private/tdd001/audit/r3-contract.json.
The frozen fixture and official results are not modified."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tdd_harness as H  # noqa: E402

CHECKS = {
    "odd_length_list": "chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]",
    "even_length_list": "chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]",
    "size_larger_than_list": "chunk([1, 2], 5) == [[1, 2]]",
    "empty_list": "chunk([], 3) == []",
    "size_one": "chunk(['a', 'b', 'c'], 1) == [['a'], ['b'], ['c']]",
    "chunks_are_lists_for_list_input": "all(isinstance(c, list) for c in chunk([1, 2, 3], 2))",
    "TUPLE_INPUT_chunks_are_lists (hidden test_returns_lists; not in the request)":
        "all(isinstance(c, list) for c in chunk((1, 2, 3), 2))",
}


def main():
    disp = {e["token"]: e for e in H.ledger_read() if e["event"] == "dispatch" and e["kind"] == "child"}
    out = {}
    for slot, r in sorted(H.valid_results("stage1").items()):
        if "/R3/" not in slot:
            continue
        src = Path(disp[r["token"]]["run_root"]) / "project"
        with tempfile.TemporaryDirectory(prefix="apsp-tdd-audit-") as td:
            work = Path(td) / "p"
            shutil.copytree(src, work, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            res = {}
            for name, expr in CHECKS.items():
                p = subprocess.run([sys.executable, "-c", f"from listkit.seq import chunk\nprint({expr})"],
                                   cwd=work, capture_output=True, text=True)
                res[name] = p.stdout.strip() == "True"
            out[slot] = {"token": r["token"], "official_M3_hidden_pass": r["M"]["M3_hidden_pass"], "checks": res,
                         "list_contract_all_pass": all(v for k, v in res.items() if not k.startswith("TUPLE"))}
    dst = H.PRIV / "audit" / "r3-contract.json"
    H.dump_json(dst, out)
    for s, v in out.items():
        print(s, "official M3:", v["official_M3_hidden_pass"], "| list contract:", v["list_contract_all_pass"],
              "| tuple:", v["checks"][[k for k in CHECKS if k.startswith("TUPLE")][0]])


if __name__ == "__main__":
    main()
