# AppleScript Adaptive Code Optimizer

This module provides an **adaptive code optimizer** written in AppleScript. It uses DeepSeek to iteratively:

1. Evaluate code quality by weighted aspects.
2. Optimize code based on those weights.
3. Repeat until quality converges or max passes is reached.

## Supported optimization aspects

You can tune each aspect weight (0.0 to 1.0):

- `performance`
- `readability`
- `safety`
- `maintainability`

Example weight profile:

```applescript
{performance:0.4, readability:0.3, safety:0.2, maintainability:0.1}
```

## Usage

Set your API key in environment variables:

```bash
export DEEPSEEK_API_KEY="your-key"
```

Then call from AppleScript:

```applescript
set sourceCode to "func sum(_ arr: [Int]) -> Int { var s = 0; for i in 0..<arr.count { s += arr[i] }; return s }"
set aspectProfile to {performance:0.45, readability:0.25, safety:0.2, maintainability:0.1}
set optimizedCode to optimizeCode(sourceCode, "Swift", aspectProfile, 3)
```

## Notes

- The evaluator prompt returns JSON (`score`, `issues`, `quick_wins`).
- The optimizer prompt returns source code only (no markdown wrappers).
- If optimization output does not look like code, the previous candidate is retained.
