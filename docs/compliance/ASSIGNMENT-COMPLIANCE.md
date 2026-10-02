# Ma trận tuân thủ yêu cầu bài tập

| Yêu cầu chính thức | Triển khai / evidence | Trạng thái | Hành động |
| --- | --- | --- | --- |
| Mục đích hệ thống, actors/use cases | `README.md`; system analysis; P0/P1 flows | COMPLETE | — |
| Source/module/dependency analysis | `docs/analysis/MODULE-DEPENDENCY-SUMMARY.md` | COMPLETE | Giới hạn module liên quan test. |
| Architecture | `docs/architecture/SYSTEM-ARCHITECTURE.md` | COMPLETE | — |
| 3–5 business/data flows | `BUSINESS-DATA-FLOWS.md` | COMPLETE | — |
| Local/Docker, versions, DB/services, QA data | `setup/`; system analysis | COMPLETE | DB/storage chỉ ở mức supported boundary. |
| System-run và >=3 flow evidence | P1 summary; `BUSINESS-FLOW-EVIDENCE.md` | COMPLETE | Retained historical evidence. |
| K05 theory/rationale, assumptions/risks | final report; analysis/design | COMPLETE | — |
| Criteria, scenarios, test data, invariants | test-design; tests; final report | COMPLETE | — |
| Automation/harness, README/dependencies | `tests/`; requirements; reproducibility guide | COMPLETE | — |
| Logs/results/metrics, defects, RCA | summaries; defect log; evidence | COMPLETE | — |
| Pin tag/commit, fresh-machine reproducibility | setup; snapshot; reproducibility guide | COMPLETE | — |
| Git history/workflow, role allocation | README; `PROJECT-WORKFLOW-EVIDENCE.md`; team roles | COMPLETE | Không suy diễn individual contribution. |
| Project/task-management board | Không có artifact Trello/Jira/GitHub Projects trong repository | NOT EVIDENCED | Chỉ bổ sung nếu nhóm có bằng chứng thật. |
| Peer evaluation | Template trống `PEER-EVALUATION-TEMPLATE.md` | PARTIAL | Nhóm hoàn thành trung thực trước nộp. |
| Final report, presentation/demo | `reports/final/`; `demo/`; submission checklist | COMPLETE | Export Word/PDF/PPT theo yêu cầu giảng viên. |

Kết luận: artefact kỹ thuật và evidence có trong repository; hai mục không thể được nâng trạng thái nếu chưa có bằng chứng ngoài repository.
