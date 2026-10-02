# Chuẩn bị hỏi đáp bảo vệ

1. **Schema-Based Testing là gì?** Sinh/kiểm tra test theo schema, ở đây là OpenAPI snapshot.
2. **Fuzz Testing là gì?** Thăm dò nhiều input, nhất là biên; đề tài giới hạn để an toàn.
3. **Schemathesis làm gì?** Đọc OpenAPI, sinh case, kiểm tra status/schema/5xx.
4. **Vì sao không test 266 operations?** Nhiều route high-risk; scope nhỏ giúp evidence và cleanup tin cậy.
5. **Vì sao chọn P0/P1?** P0 GET trước; P1 write lifecycle sau khi có guardrail.
6. **DEF-02 là backend defect?** Là contract/documentation mismatch: runtime 400 không được schema mô tả.
7. **404 luôn là bug?** Không; DEF-03 là defect vì OpenAPI thiếu 404 response.
8. **DEF-04 FAIL sao là kết quả đúng?** Contract đòi 201/422, runtime 500; FAIL giữ defect detector.
9. **Vì sao DEF-01 chưa confirmed RCA?** Thiếu stack trace/database diagnostic dù source cho path khả dĩ.
10. **Tái lập bằng cách nào?** Pin commit/snapshot/dependencies, guide, health check và evidence map.
11. **Vì sao không commit token?** Token là credential, commit tạo rủi ro truy cập.
12. **Oracle là gì?** Quy tắc pass/fail, ví dụ status phải thuộc response map.
13. **Invariant là gì?** Tính chất luôn giữ trong scope, ví dụ input biên không gây undocumented 5xx.
14. **Hạn chế OpenAPI?** Không đủ mô tả ownership, rollback, idempotency và có thể thiếu error response.
15. **P0 có pass không?** 9/9 được exercise nhưng có known detections, không all-pass.
16. **P1 có an toàn?** Unique QA resource, cleanup child trước parent, không broad-fuzz.
17. **P5 có replay authenticated không?** Không; token thiếu trong process, chỉ tổng hợp P3/P4 evidence và ghi rõ điều đó.
