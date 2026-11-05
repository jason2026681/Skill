#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产资料归档评审问题清单生成器
用法:
    python generate_report.py --project "产品型号" --type initial|change --json findings.json --out 问题清单.xlsx

findings.json 结构:
{
  "project": "产品型号/单板名",
  "review_type": "initial" | "change",
  "reviewer": "评审人(可选)",
  "date": "2026-10-20",
  "spec_version": "本次评审依据的公司规范版本(可选)",
  "findings": [
    {
      "id": "B1-04",
      "category": "整机BOM",
      "item": "关键器件有完整制造商料号",
      "evidence": "U3 主控料号缺失"
    }
  ]
}

说明: 只输出检查出的问题项，无结论、无严重度、无整改建议。
"""
import argparse
import json
import sys

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: openpyxl not installed. Install with: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

THIN = Side(style="thin", color="999999")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD_FILL = PatternFill("solid", fgColor="1F4E79")
HEAD_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
META_FONT = Font(name="微软雅黑", size=10, color="595959")
BODY_FONT = Font(name="微软雅黑", size=10)
WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def build_report(data: dict, out_path: str) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "问题清单"

    # ---------- 表头上方信息区 ----------
    ws["A1"] = "生产资料归档合规性评审——问题清单"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:E1")
    ws.row_dimensions[1].height = 26

    meta = [
        ("评审对象", data.get("project", "")),
        ("评审类型", "初次归档评审" if data.get("review_type") == "initial" else "变更评审"),
        ("评审日期", data.get("date", "")),
    ]
    if data.get("reviewer"):
        meta.append(("评审人", data["reviewer"]))
    if data.get("spec_version"):
        meta.append(("规范版本", data["spec_version"]))

    for i, (k, v) in enumerate(meta, start=2):
        ws.cell(row=i, column=1, value=k).font = META_FONT
        ws.cell(row=i, column=1).alignment = CENTER
        c = ws.cell(row=i, column=2, value=v)
        c.font = META_FONT
        c.alignment = WRAP
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=5)

    # ---------- 问题清单表 ----------
    header_row = len(meta) + 3
    headers = ["序号", "检查项编号", "类别", "检查项", "问题描述"]
    for j, h in enumerate(headers, start=1):
        c = ws.cell(row=header_row, column=j, value=h)
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = CENTER
        c.border = BORDER
    ws.row_dimensions[header_row].height = 22
    ws.freeze_panes = f"A{header_row + 1}"

    findings = data.get("findings", [])
    for i, f in enumerate(findings, start=1):
        row = header_row + i
        values = [
            i,
            f.get("id", ""),
            f.get("category", ""),
            f.get("item", ""),
            f.get("evidence", ""),
        ]
        for j, v in enumerate(values, start=1):
            c = ws.cell(row=row, column=j, value=v)
            c.font = BODY_FONT
            c.border = BORDER
            c.alignment = CENTER if j in (1, 2, 3) else WRAP

    if not findings:
        c = ws.cell(row=header_row + 1, column=1, value="未检查出问题项")
        c.font = META_FONT
        c.alignment = CENTER
        ws.merge_cells(start_row=header_row + 1, start_column=1, end_row=header_row + 1, end_column=5)

    widths = [6, 13, 12, 36, 52]
    for j, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w

    wb.save(out_path)
    print(f"OK: report saved to {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="", help="评审对象（产品/单板名），留空则取 json 内字段")
    ap.add_argument("--type", choices=["initial", "change"], default=None)
    ap.add_argument("--json", required=True, help="findings JSON 文件路径")
    ap.add_argument("--out", required=True, help="输出 xlsx 路径")
    args = ap.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)
    if args.project:
        data["project"] = args.project
    if args.type:
        data["review_type"] = args.type

    build_report(data, args.out)


if __name__ == "__main__":
    main()
