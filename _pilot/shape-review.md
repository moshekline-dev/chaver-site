# Shape Mismatch Review — 27 Chapters (20 original + 7 from Pass 3.5)

**Date:** 2026-05-10
**Purpose:** These 20 chapters have matching docx tables but different row/column
structures. Moshe needs to decide for each: is the JSON shape correct, the docx shape
correct, or do both need revision?

---

## avot_2

| Field | JSON | Docx |
|---|---|---|
| tractate | avot (אבות) | — |
| seder | Nezikin | — |
| chapter | 2 | — |
| rows | 6 | 8 |
| shape (cells/row) | [1, 3, 4, 4, 6, 2] | [1, 3, 4, 1, 3, 1, 5, 2] |
| difference | Docx has 2 extra row(s) — docx starts with full-width title row |
| first cell text | רבי אומר איזו היא דרך ישרה שיבר לו האדם כל שהיא תפארת לעשיה  |

**Decision:** [pending]

---

## eduyot_7

| Field | JSON | Docx |
|---|---|---|
| tractate | eduyot (עדויות) | — |
| seder | Nezikin | — |
| chapter | 7 | — |
| rows | 2 | 6 |
| shape (cells/row) | [3, 3] | [2, 2, 2, 2, 2, 2] |
| difference | Docx has 4 extra row(s) |
| first cell text | העיד רבי יהושע ורבי צדוק
על פדיון פטר חמור שמת
שאין בו לכהן  |

**Decision:** [pending]

---

## kelim_4

| Field | JSON | Docx |
|---|---|---|
| tractate | kelim (כלים) | — |
| seder | Toharot | — |
| chapter | 4 | — |
| rows | 2 | 2 |
| shape (cells/row) | [3, 3] | [2, 2] |
| difference | Same row count, different cell counts |
| first cell text | שולי קרפיות
ושולי קוסים הצידוניים
אף על פי שאינם יכולים לישב |

**Decision:** [pending]

---

## keritot_4

| Field | JSON | Docx |
|---|---|---|
| tractate | keritot (כריתות) | — |
| seder | Kodashim | — |
| chapter | 4 | — |
| rows | 2 | 5 |
| shape (cells/row) | [3, 3] | [2, 2, 3, 3, 3] |
| difference | Docx has 3 extra row(s) |
| first cell text | ספק אכל חלב ספק לא אכל
ואפלו אכל
ספק יש בו כשעור ספק שאין בו |

**Decision:** [pending]

---

## ketubot_11

| Field | JSON | Docx |
|---|---|---|
| tractate | ketubot (כתובות) | — |
| seder | Nashim | — |
| chapter | 11 | — |
| rows | 5 | 3 |
| shape (cells/row) | [1, 2, 1, 2, 1] | [1, 2, 1] |
| difference | JSON has 2 extra row(s) |
| first cell text | אלמנה נזונת מנכסי יתומים
מעשה ידיה שלהן ואין חיבין בקבורתה
י |

**Decision:** [pending]

---

## kinnim_1

| Field | JSON | Docx |
|---|---|---|
| tractate | kinnim (קנים) | — |
| seder | Kodashim | — |
| chapter | 1 | — |
| rows | 2 | 3 |
| shape (cells/row) | [5, 4] | [3, 3, 3] |
| difference | Docx has 1 extra row(s) |
| first cell text | סדר קנים כך הוא
החובה אחד חטאת ואחד עולה
בנדרים ובנדבות כלן  |

**Decision:** [pending]

---

## makkot_1

| Field | JSON | Docx |
|---|---|---|
| tractate | makkot (מכות) | — |
| seder | Nezikin | — |
| chapter | 1 | — |
| rows | 4 | 5 |
| shape (cells/row) | [4, 3, 3, 3] | [1, 3, 3, 3, 3] |
| difference | Docx has 1 extra row(s) — docx starts with full-width title row |
| first cell text | כיצד העדים נעשים זוממין |

**Decision:** [pending]

---

## makkot_2

| Field | JSON | Docx |
|---|---|---|
| tractate | makkot (מכות) | — |
| seder | Nezikin | — |
| chapter | 2 | — |
| rows | 4 | 5 |
| shape (cells/row) | [4, 3, 3, 3] | [1, 3, 3, 3, 3] |
| difference | Docx has 1 extra row(s) — docx starts with full-width title row |
| first cell text | אלו הן הגולין |

**Decision:** [pending]

---

## makkot_3

| Field | JSON | Docx |
|---|---|---|
| tractate | makkot (מכות) | — |
| seder | Nezikin | — |
| chapter | 3 | — |
| rows | 5 | 6 |
| shape (cells/row) | [4, 2, 2, 2, 3] | [1, 3, 2, 2, 2, 3] |
| difference | Docx has 1 extra row(s) — docx starts with full-width title row |
| first cell text | ואלו הן הלוקין |

**Decision:** [pending]

---

## meilah_1

| Field | JSON | Docx |
|---|---|---|
| tractate | meilah (מעילה) | — |
| seder | Kodashim | — |
| chapter | 1 | — |
| rows | 4 | 5 |
| shape (cells/row) | [2, 2, 3, 1] | [2, 2, 1, 2, 1] |
| difference | Docx has 1 extra row(s) |
| first cell text | קדשי קדשים ששחטן בדרום מועלים בהן
שחטן בדרום וקבל דמן בצפון
 |

**Decision:** [pending]

---

## niddah_3

| Field | JSON | Docx |
|---|---|---|
| tractate | niddah (נידה) | — |
| seder | Toharot | — |
| chapter | 3 | — |
| rows | 3 | 4 |
| shape (cells/row) | [3, 3, 6] | [3, 3, 3, 3] |
| difference | Docx has 1 extra row(s) |
| first cell text | המפלת חתיכה
אם יש עמה דם טמאה
ואם לאו טהורה
רבי יהודה אומר
ב |

**Decision:** [pending]

---

## sanhedrin_11

| Field | JSON | Docx |
|---|---|---|
| tractate | sanhedrin (סנהדרין) | — |
| seder | Nezikin | — |
| chapter | 11 | — |
| rows | 5 | 6 |
| shape (cells/row) | [3, 3, 3, 3, 2] | [1, 2, 3, 3, 3, 2] |
| difference | Docx has 1 extra row(s) — docx starts with full-width title row |
| first cell text | אלו הן הנחנקין
המכה אביו ואמו והגונב נפש מישראל
וזקן ממרא על |

**Decision:** [pending]

---

## sanhedrin_6

| Field | JSON | Docx |
|---|---|---|
| tractate | sanhedrin (סנהדרין) | — |
| seder | Nezikin | — |
| chapter | 6 | — |
| rows | 4 | 4 |
| shape (cells/row) | [4, 3, 3, 3] | [3, 3, 3, 3] |
| difference | Same row count, different cell counts |
| first cell text | נגמר הדין מוציאין אותו לסקלו |

**Decision:** [pending]

---

## sanhedrin_7

| Field | JSON | Docx |
|---|---|---|
| tractate | sanhedrin (סנהדרין) | — |
| seder | Nezikin | — |
| chapter | 7 | — |
| rows | 2 | 4 |
| shape (cells/row) | [4, 4] | [1, 3, 1, 3] |
| difference | Docx has 2 extra row(s) — docx starts with full-width title row |
| first cell text | ארבע מיתות נמסרו לבית דין סקילה שרפה הרג וחנק
רבי שמעון אומר |

**Decision:** [pending]

---

## shevuot_3

| Field | JSON | Docx |
|---|---|---|
| tractate | shevuot (שבועות) | — |
| seder | Nezikin | — |
| chapter | 3 | — |
| rows | 5 | 6 |
| shape (cells/row) | [2, 4, 2, 2, 2] | [2, 2, 2, 2, 2, 2] |
| difference | Docx has 1 extra row(s) |
| first cell text | שבועות שתים שהן ארבע
שבועה שאכל ושלא אכל
שאכלתי ושלא אכלתי |

**Decision:** [pending]

---

## shevuot_6

| Field | JSON | Docx |
|---|---|---|
| tractate | shevuot (שבועות) | — |
| seder | Nezikin | — |
| chapter | 6 | — |
| rows | 4 | 5 |
| shape (cells/row) | [4, 3, 3, 3] | [1, 3, 3, 3, 3] |
| difference | Docx has 1 extra row(s) — docx starts with full-width title row |
| first cell text | שבועת הדינין
הטענה שתי כסף וההודאה בשוה פרוטה ואם אין ההודאה |

**Decision:** [pending]

---

## shevuot_8

| Field | JSON | Docx |
|---|---|---|
| tractate | shevuot (שבועות) | — |
| seder | Nezikin | — |
| chapter | 8 | — |
| rows | 3 | 4 |
| shape (cells/row) | [3, 3, 2] | [1, 2, 3, 2] |
| difference | Docx has 1 extra row(s) — docx starts with full-width title row |
| first cell text | ארבעה שומרים הן
שומר חנם והשואל נושא שכר והשוכר |

**Decision:** [pending]

---

## tahorot_1

| Field | JSON | Docx |
|---|---|---|
| tractate | tahorot (טהרות) | — |
| seder | Toharot | — |
| chapter | 1 | — |
| rows | 3 | 4 |
| shape (cells/row) | [3, 4, 3] | [3, 1, 3, 3] |
| difference | Docx has 1 extra row(s) |
| first cell text | שלשה עשר דבר בנבלת העוף הטהור
צריכה מחשבה ואינה צריכה הכשר
ו |

**Decision:** [pending]

---

## temurah_7

| Field | JSON | Docx |
|---|---|---|
| tractate | temurah (תמורה) | — |
| seder | Kodashim | — |
| chapter | 7 | — |
| rows | 3 | 4 |
| shape (cells/row) | [3, 3, 2] | [2, 2, 2, 2] |
| difference | Docx has 1 extra row(s) |
| first cell text | יש בקדשי המזבח מה שאין בקדשי בדק הבית
ויש בקדשי בדק הבית מה  |

**Decision:** [pending]

---

## yevamot_2

| Field | JSON | Docx |
|---|---|---|
| tractate | yevamot (יבמות) | — |
| seder | Nashim | — |
| chapter | 2 | — |
| rows | 2 | 5 |
| shape (cells/row) | [3, 3] | [2, 2, 2, 2, 2] |
| difference | Docx has 3 extra row(s) |
| first cell text |  |

**Decision:** [pending]

---

# Additional Chapters (from Pass 3.5)

These 7 chapters were previously **unmatched** (no table found due to extractor bugs).
After the v2.1 bug fixes (reversed headers, gematria, key aliases), their tables are now
found — but their shapes don't match the JSON. Total shape-mismatch set: 20 + 7 = 27.

**Note:** The Pass 3.5 report stated "6 new shape mismatches." The actual count is 7.
The discrepancy is likely a counting error during the earlier session. No overlaps with
the original 20. Two chapters from the original 20 (`keritot_4`, `kinnim_1`) were not
re-found in this scan — their docx tables may use a header variant not captured by the
standard/reversed two-orientation check.

---

## bekhorot_8

| Field | JSON | Docx |
|---|---|---|
| tractate | bekhorot (בכורות) | — |
| seder | Kodashim | — |
| chapter | 8 | — |
| rows | 3 | 4 |
| shape (cells/row) | [4, 3, 3] | [1, 3, 3, 3] |
| difference | Docx has 1 extra row — docx starts with full-width title row |
| first cell text | יש בכור לנחלה ואינו בכור לכהן בכור לכהן ואינו בכור לנחלה בכור ל |

**Decision:** [pending]

---

## keritot_3

| Field | JSON | Docx |
|---|---|---|
| tractate | keritot (כריתות) | — |
| seder | Kodashim | — |
| chapter | 3 | — |
| rows | 2 | 5 |
| shape (cells/row) | [2, 2] | [2, 2, 3, 3, 3] |
| difference | Docx has 3 extra rows — fundamentally different structure |
| first cell text | אכל חלב וחלב בהעלם אחד אינו חיב אלא חטאת אחת אכל חלב ודם ונות |

**Decision:** [pending]

---

## ketubot_12

| Field | JSON | Docx |
|---|---|---|
| tractate | ketubot (כתובות) | — |
| seder | Nashim | — |
| chapter | 12 | — |
| rows | 3 | 2 |
| shape (cells/row) | [1, 2, 1] | [3, 3] |
| difference | JSON has 1 extra row; cell counts differ — different structural analysis |
| first cell text | הנושא את האשה ופסקה עמו כדי שיזון את בתה חמש שנים חיב לזונה חמ |

**Decision:** [pending]

---

## sanhedrin_1

| Field | JSON | Docx |
|---|---|---|
| tractate | sanhedrin (סנהדרין) | — |
| seder | Nezikin | — |
| chapter | 1 | — |
| rows | 3 | 5 |
| shape (cells/row) | [3, 2, 3] | [3, 2, 3, 3, 3] |
| difference | Docx has 2 extra rows |
| first cell text | עבור החדש בשלשה עבור השנה בשלשה דברי רבי מאיר רבן שמעון בן גמלי |

**Decision:** [pending]

---

## yadayim_3

| Field | JSON | Docx |
|---|---|---|
| tractate | yadayim (ידים) | — |
| seder | Toharot | — |
| chapter | 3 | — |
| rows | 3 | 6 |
| shape (cells/row) | [2, 2, 2] | [2, 2, 2, 3, 2, 2] |
| difference | Docx has 3 extra rows |
| first cell text | האכלין והכלים שנטמאו במשקין מטמאין את הידים להיות שניות דברי רבי |

**Decision:** [pending]

---

## zevachim_5

| Field | JSON | Docx |
|---|---|---|
| tractate | zevachim (זבחים) | — |
| seder | Kodashim | — |
| chapter | 5 | — |
| rows | 3 | 5 |
| shape (cells/row) | [3, 2, 3] | [1, 2, 3, 2, 1] |
| difference | Docx has 2 extra rows — docx starts with full-width title row; different cell distribution |
| first cell text | איזהו מקומן שלזבחים קדשי קדשים שחיטתן בצפון |

**Decision:** [pending]

---

## zevachim_6

| Field | JSON | Docx |
|---|---|---|
| tractate | zevachim (זבחים) | — |
| seder | Kodashim | — |
| chapter | 6 | — |
| rows | 3 | 4 |
| shape (cells/row) | [2, 2, 4] | [2, 2, 2, 2] |
| difference | Docx has 1 extra row; last row differs (JSON has 4 cells, docx splits into 2+2) |
| first cell text | חטאת העוף היתה נעשית על קרן דרומית מערבית בכל מקום היתה כשרה אל |

**Decision:** [pending]

---
