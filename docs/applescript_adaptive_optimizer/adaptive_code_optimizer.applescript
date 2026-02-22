-- Adaptive Code Optimizer for AppleScript + DeepSeek API
-- Usage:
-- set optimized to optimizeCode(sourceCode, "Swift", {performance:0.4, readability:0.3, safety:0.2, maintainability:0.1}, 2)

on optimizeCode(codeText, targetLanguage, aspectWeights, maxPasses)
	set apiKey to my requireEnv("DEEPSEEK_API_KEY")
	set modelName to "deepseek-chat"
	set passCount to 1
	set candidate to codeText
	
	repeat while passCount ≤ maxPasses
		set evaluationPrompt to my buildEvaluationPrompt(candidate, targetLanguage, aspectWeights)
		set evalResp to my callDeepSeek(apiKey, modelName, evaluationPrompt, 0.1)
		set evalJSON to my jsonStringValue(evalResp, "content")
		set evalScore to my parseScore(evalJSON)
		
		set optimizePrompt to my buildOptimizationPrompt(candidate, targetLanguage, aspectWeights, evalJSON)
		set nextResp to my callDeepSeek(apiKey, modelName, optimizePrompt, 0.25)
		set nextCode to my jsonStringValue(nextResp, "content")
		
		if (my looksLikeCode(nextCode)) then set candidate to nextCode
		if evalScore ≥ 95 then exit repeat
		set passCount to passCount + 1
	end repeat
	
	return candidate
end optimizeCode

on buildEvaluationPrompt(codeText, targetLanguage, aspectWeights)
	set perfWeight to performance of aspectWeights
	set readWeight to readability of aspectWeights
	set safeWeight to safety of aspectWeights
	set maintWeight to maintainability of aspectWeights
	
	return "You are a strict code reviewer. Evaluate the code from 0 to 100 using weighted aspects. " & ¬
		"Language: " & targetLanguage & ". " & ¬
		"Weights: performance=" & perfWeight & ", readability=" & readWeight & ", safety=" & safeWeight & ", maintainability=" & maintWeight & ". " & ¬
		"Return JSON only, format: {\"score\":number,\"issues\":[string],\"quick_wins\":[string]}.\n\nCode:\n```\n" & codeText & "\n```"
end buildEvaluationPrompt

on buildOptimizationPrompt(codeText, targetLanguage, aspectWeights, reviewJSON)
	set perfWeight to performance of aspectWeights
	set readWeight to readability of aspectWeights
	set safeWeight to safety of aspectWeights
	set maintWeight to maintainability of aspectWeights
	
	return "You are an adaptive code optimizer. Improve the code while preserving behavior. " & ¬
		"Language: " & targetLanguage & ". " & ¬
		"Optimization priorities: performance=" & perfWeight & ", readability=" & readWeight & ", safety=" & safeWeight & ", maintainability=" & maintWeight & ". " & ¬
		"Use this review feedback JSON: " & reviewJSON & ". " & ¬
		"Return only the optimized source code, no markdown fences, no explanation.\n\nOriginal code:\n" & codeText
end buildOptimizationPrompt

on callDeepSeek(apiKey, modelName, promptText, tempValue)
	set py to "import json, os, sys, urllib.request\n" & ¬
		"api_key = os.environ['DEEPSEEK_API_KEY']\n" & ¬
		"model = sys.argv[1]\n" & ¬
		"temperature = float(sys.argv[2])\n" & ¬
		"prompt = sys.stdin.read()\n" & ¬
		"payload = {\"model\": model, \"temperature\": temperature, \"messages\": [{\"role\": \"user\", \"content\": prompt}]}\n" & ¬
		"data = json.dumps(payload).encode('utf-8')\n" & ¬
		"req = urllib.request.Request('https://api.deepseek.com/chat/completions', data=data, headers={\"Authorization\": f\"Bearer {api_key}\", \"Content-Type\": \"application/json\"})\n" & ¬
		"with urllib.request.urlopen(req, timeout=60) as r:\n" & ¬
		"    obj = json.loads(r.read().decode('utf-8'))\n" & ¬
		"print(json.dumps({\"content\": obj['choices'][0]['message']['content']}))\n"
	
	set shellCmd to "python3 -c " & quoted form of py & " " & quoted form of modelName & " " & quoted form of (tempValue as text)
	set rawResult to do shell script "DEEPSEEK_API_KEY=" & quoted form of apiKey & " " & shellCmd & " <<'PROMPT'\n" & promptText & "\nPROMPT"
	return rawResult
end callDeepSeek

on requireEnv(envName)
	try
		set envVal to do shell script "printenv " & envName
		if envVal is "" then error "Missing env var: " & envName
		return envVal
	on error
		error "Missing env var: " & envName
	end try
end requireEnv

on parseScore(reviewJSON)
	try
		set py to "import json,sys\nobj=json.loads(sys.stdin.read())\nprint(int(obj.get('score',0)))"
		set val to do shell script "python3 -c " & quoted form of py & " <<'JSON'\n" & reviewJSON & "\nJSON"
		return val as integer
	on error
		return 0
	end try
end parseScore

on jsonStringValue(jsonBlob, keyName)
	set py to "import json,sys\nobj=json.loads(sys.stdin.read())\nprint(obj.get(sys.argv[1],''))"
	return do shell script "python3 -c " & quoted form of py & " " & quoted form of keyName & " <<'JSON'\n" & jsonBlob & "\nJSON"
end jsonStringValue

on looksLikeCode(candidateText)
	if candidateText is "" then return false
	if candidateText contains "{\"score\"" then return false
	return true
end looksLikeCode
