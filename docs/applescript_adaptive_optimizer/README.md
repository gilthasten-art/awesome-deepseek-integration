# AppleScript Adaptive Code Optimizer

This guide provides an **adaptive code optimizer** written in AppleScript. It evaluates code quality from multiple aspects inspired by AppleScript constant categories:

- Arithmetic logic
- Boolean logic
- Date/time handling
- String handling
- Script constant safety

The optimizer updates aspect weights based on feedback, so repeated runs become more tailored to your coding style and quality goals.

## AppleScript Optimizer Script

```applescript
(***
Adaptive Code Optimizer for AppleScript-like logic reviews
- Aspect scoring
- Weighted total score
- Adaptive weight updates from feedback
***)

script AdaptiveCodeOptimizer
	property aspectWeights : {arithmetic:1.0, booleanLogic:1.0, dateTime:1.0, stringHandling:1.0, scriptConstants:1.0}
	property learningRate : 0.15
	property minWeight : 0.2
	property maxWeight : 3.0
	
	on optimizeCode(codeText)
		set aspectScores to evaluateAspects(codeText)
		set weightedScore to calculateWeightedScore(aspectScores)
		set recommendations to buildRecommendations(codeText, aspectScores)
		
		return {scores:aspectScores, totalScore:weightedScore, recommendations:recommendations, activeWeights:aspectWeights}
	end optimizeCode
	
	on learnFromFeedback(aspectScores, userSatisfaction)
		-- userSatisfaction expected range: 0.0 .. 1.0
		if userSatisfaction < 0.0 then set userSatisfaction to 0.0
		if userSatisfaction > 1.0 then set userSatisfaction to 1.0
		
		set targetQuality to userSatisfaction * 100
		
		set arithmeticDelta to ((targetQuality - (arithmetic of aspectScores)) / 100) * learningRate
		set booleanDelta to ((targetQuality - (booleanLogic of aspectScores)) / 100) * learningRate
		set dateDelta to ((targetQuality - (dateTime of aspectScores)) / 100) * learningRate
		set stringDelta to ((targetQuality - (stringHandling of aspectScores)) / 100) * learningRate
		set constantsDelta to ((targetQuality - (scriptConstants of aspectScores)) / 100) * learningRate
		
		set arithmetic of aspectWeights to clampWeight((arithmetic of aspectWeights) + arithmeticDelta)
		set booleanLogic of aspectWeights to clampWeight((booleanLogic of aspectWeights) + booleanDelta)
		set dateTime of aspectWeights to clampWeight((dateTime of aspectWeights) + dateDelta)
		set stringHandling of aspectWeights to clampWeight((stringHandling of aspectWeights) + stringDelta)
		set scriptConstants of aspectWeights to clampWeight((scriptConstants of aspectWeights) + constantsDelta)
		
		return aspectWeights
	end learnFromFeedback
	
	on evaluateAspects(codeText)
		set arithmeticScore to evaluateArithmetic(codeText)
		set booleanScore to evaluateBooleanLogic(codeText)
		set dateScore to evaluateDateTime(codeText)
		set stringScore to evaluateStringHandling(codeText)
		set constantsScore to evaluateScriptConstants(codeText)
		
		return {arithmetic:arithmeticScore, booleanLogic:booleanScore, dateTime:dateScore, stringHandling:stringScore, scriptConstants:constantsScore}
	end evaluateAspects
	
	on calculateWeightedScore(aspectScores)
		set weightedSum to ((arithmetic of aspectScores) * (arithmetic of aspectWeights)) + ¬
			((booleanLogic of aspectScores) * (booleanLogic of aspectWeights)) + ¬
			((dateTime of aspectScores) * (dateTime of aspectWeights)) + ¬
			((stringHandling of aspectScores) * (stringHandling of aspectWeights)) + ¬
			((scriptConstants of aspectScores) * (scriptConstants of aspectWeights))
		
		set weightSum to (arithmetic of aspectWeights) + (booleanLogic of aspectWeights) + (dateTime of aspectWeights) + (stringHandling of aspectWeights) + (scriptConstants of aspectWeights)
		
		if weightSum is 0 then return 0
		return round (weightedSum / weightSum)
	end calculateWeightedScore
	
	on buildRecommendations(codeText, aspectScores)
		set recs to {}
		
		if (arithmetic of aspectScores) < 70 then set end of recs to "Arithmetic: simplify formulas and reuse constants such as pi when relevant."
		if (booleanLogic of aspectScores) < 70 then set end of recs to "Boolean logic: reduce nested conditions and prefer explicit true/false branches."
		if (dateTime of aspectScores) < 70 then set end of recs to "Date/time: prefer built-in constants like minutes, hours, days, weeks for clarity."
		if (stringHandling of aspectScores) < 70 then set end of recs to "String handling: standardize with constants like return, space, and tab for formatting."
		if (scriptConstants of aspectScores) < 70 then set end of recs to "Script constants: verify use of current application, me, it, and missing value for safer scripts."
		
		if (count of recs) is 0 then set recs to {"Great job. All aspects are above the target threshold."}
		return recs
	end buildRecommendations
	
	on evaluateArithmetic(codeText)
		set score to 60
		if codeText contains "pi" then set score to score + 20
		if codeText contains "+" or codeText contains "-" or codeText contains "*" or codeText contains "/" then set score to score + 15
		if codeText contains "mod" then set score to score + 5
		return clampScore(score)
	end evaluateArithmetic
	
	on evaluateBooleanLogic(codeText)
		set score to 60
		if codeText contains "true" then set score to score + 10
		if codeText contains "false" then set score to score + 10
		if codeText contains "if" then set score to score + 10
		if codeText contains "and" or codeText contains "or" then set score to score + 10
		return clampScore(score)
	end evaluateBooleanLogic
	
	on evaluateDateTime(codeText)
		set score to 55
		if codeText contains "current date" then set score to score + 20
		if codeText contains "minutes" or codeText contains "hours" or codeText contains "days" or codeText contains "weeks" then set score to score + 20
		if codeText contains "date" then set score to score + 10
		return clampScore(score)
	end evaluateDateTime
	
	on evaluateStringHandling(codeText)
		set score to 55
		if codeText contains "return" then set score to score + 15
		if codeText contains "space" then set score to score + 10
		if codeText contains "tab" then set score to score + 10
		if codeText contains "text" then set score to score + 10
		return clampScore(score)
	end evaluateStringHandling
	
	on evaluateScriptConstants(codeText)
		set score to 50
		if codeText contains "current application" then set score to score + 15
		if codeText contains "me" then set score to score + 10
		if codeText contains "it" then set score to score + 10
		if codeText contains "missing value" then set score to score + 15
		if codeText contains "result" then set score to score + 10
		return clampScore(score)
	end evaluateScriptConstants
	
	on clampScore(v)
		if v < 0 then return 0
		if v > 100 then return 100
		return v
	end clampScore
	
	on clampWeight(v)
		if v < minWeight then return minWeight
		if v > maxWeight then return maxWeight
		return v
	end clampWeight
end script
```

## Example usage

```applescript
set sampleCode to "set x to pi * 2
if true and false then
	set d to current date + 2 * days
end if
set output to \"A\" & return & \"B\" & space & \"C\"
"

set analysisResult to AdaptiveCodeOptimizer's optimizeCode(sampleCode)
set currentScores to scores of analysisResult

-- Simulate human feedback (0.0..1.0)
set updatedWeights to AdaptiveCodeOptimizer's learnFromFeedback(currentScores, 0.85)

return {analysisResult, updatedWeights}
```

## What makes it adaptive?

- Each aspect has a weight.
- After every run, feedback (`userSatisfaction`) nudges weights.
- Lower-performing aspects for your target quality gain weight over time.
- Weights are bounded to avoid instability.

This gives you an optimizer that evolves with your expectations instead of using fixed scoring forever.
