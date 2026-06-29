# Implementation Plan for UI/UX Enhancements

## Goal
Improve storytelling, visual hierarchy, and usability of the existing Streamlit dashboard while preserving all core functionality and calculations.

## Changes Overview
| # | Section | Description |
|---|---------|-------------|
| 1 | Header (Hero) | Replace plain text banner with a styled hero container containing the project title, tagline, and a concise workflow diagram with optional icons. |
| 2 | Dataset Explorer | Re‑arrange the three selectors (Fog Density, Image Type, Sample Image) into a horizontal layout using `st.columns` to reduce vertical scrolling. |
| 3 | Dehazing Comparison | Rename caption "Original Foggy Image" → "Foggy Input" and add short explanatory captions for each column (Reduced visibility, Basic enhancement, Advanced visibility recovery). |
| 4 | Detection Comparison | Add a subtitle, rename column captions (Fog Detection, Simple DCP Detection, Full DCP Detection) and place captions underneath images. |
| 5 | Detection Improvement Summary | Insert a new compact table directly below Detection Comparison showing **Metric**, **Fog**, **Full DCP** values (Detection Count, Average Confidence, PRI) and generate a one‑sentence insight. |
| 6 | Plot Height Reduction | Decrease the height of the two detection plots (e.g., `height=300`). |
| 7 | Metrics Table Redesign | Rename the section to **Quantitative Comparison**, use a cleaner `st.dataframe` style, and highlight the columns **Full DCP Count**, **Full DCP Avg Conf**, **Full DCP PRI**. |
| 8 | Perception Analysis | Keep KPI cards but update labels to *Objects Detected*, *Detection Confidence*, *Proposed PRI* and improve the interpretation text (Degradation, Minimal Recovery, Moderate Recovery, Strong Recovery). |
| 9 | Safety Assessment | Replace plain metric values with colored badge style (🟢 LOW, 🟡 MODERATE, 🔴 HIGH). Add visual emphasis around the three metrics (risk, speed, stopping distance). |
|10| Safety Summary Rewrite | Replace the generated text with a professional research insight. |
|11| Key Insight Panel | Add a final section titled **Key Insight** summarising the end‑to‑end story (Computer Vision → Object Detection → PRI → Transportation Safety). |

## Detailed Implementation Steps (see discussion) 
- Header hero markup with CSS.
- Dataset explorer using `st.columns`.
- Updated captions and subtitles.
- New detection improvement summary table using `st.table`.
- Reduce plot heights via `height=300`.
- Redesign metrics table with highlighted columns using pandas Styler.
- Update KPI labels and interpretation.
- Badge styling for safety risk.
- Rewrite safety summary text.
- Append Key Insight panel at end of file.

## Open Questions for the User
- Preferred color palette or icons for the hero workflow?
- Badge styling preference (emoji vs custom CSS colors)?
- Desired plot height (300 px suggested)?
- Any corporate style guidelines (fonts, colors) to embed?

## Verification Plan
1. Run `streamlit run app.py` and manually verify UI changes.
2. Ensure existing functionality (CSV loading, image selection, metric calculations) still works.
3. No new runtime errors.
4. Validate new tables and captions display correct values from `summary_df`.
5. Confirm safety summary still uses `sd.summarize` output.

Please review the plan and answer the open questions. Once approved, I will apply the modifications.
