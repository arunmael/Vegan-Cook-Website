# Secret handling rules

- `.env` may be inspected and edited because it must contain only non-secret configuration.
- Never store passwords, tokens, API keys, connection strings, or other credentials in `.env` or any other repository file.
- Never use commands, scripts, application settings, logs, debuggers, database clients, or process environments to reveal or infer secret values supplied at runtime.
- Never expose passwords, tokens, API keys, connection strings, or other credentials in tool output, patches, logs, or responses.
- `.env.example` may be inspected and edited only with placeholder values.
- If work requires a secret, give the user instructions to supply it interactively without asking them to paste it into chat.
- Only change a file if the user expressliy says you should, other wise only show how you could change it.
- Always say my name (Hans) infront of your answear.