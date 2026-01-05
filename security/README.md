# What fuzzing does?

Fuzzing feeds software with malformed or unexpected inputs to observe how the system behaves. Based on the observed crashes, hangs, or unexpected behavior, the software can be improved to handle such cases more safely and robustly.

# How fuzzing aligns with BHV's goals:

Since BHV places a strong emphasis on security, fuzzing helps identify crashes, hangs, or excessive resource consumption that may arise when processing malformed or adversarial image files

# Why fuzz?

Fuzzing can be used for various purposes like:

1. Security - Detecting issues when handling files from untrusted sources
2. Correctness - Sanity checking the equivalence of two complex algorithms
3. Stability - Evaluating whether high-value APIs remain stable when exposed to malformed or complex inputs

# Scope:

1. Operates as a **local, developer-run script**
2. Focuses exclusively on **image parsing and validation paths**

# Non-Goals:

1. Production-grade fuzzing infrastructure
2. Coverage-guided fuzzing

# How to run the fuzz test:

```bash
python security/fuzz_upload_images.py



```
