# Use DataPorium with AI assistants through MCP

DataPorium runs a Model Context Protocol (MCP) server. Connect it once and Claude, ChatGPT, Cursor and other AI assistants get 46 tools that read the same data as the REST API. You then ask in plain language. The server is remote, so there is nothing to install.

| | |
|---|---|
| Server address | `https://mcp.dataporium.io/mcp` |
| Transport | Streamable HTTP |
| Health check | <https://mcp.dataporium.io/health> |

The setup steps below follow the [MCP page](https://dataporium.tech/mcp) and the MCP section of the [API documentation](https://dataporium.tech/api-docs#mcp). If this page and the website ever differ, the website is right.

## Your API key

Every call uses your own API key, so your plan limits apply exactly as they do for the REST API. MCP access is included with the Premium plan; see [pricing](https://dataporium.tech/pricing). Your API key is in your account settings once you subscribe, and the same key works for the REST API.

The server accepts the key in three ways:

| Way | Example |
|---|---|
| `Authorization` header | `Authorization: Bearer YOUR_API_KEY` |
| `X-API-Key` header | `X-API-Key: YOUR_API_KEY` |
| In the address, for apps that only accept a URL | `https://mcp.dataporium.io/mcp?apikey=YOUR_API_KEY` |

Replace `YOUR_API_KEY` with your own key in every example.

## Claude (web, desktop and mobile)

Works in Claude.ai, Claude Desktop and the Claude mobile apps. Custom connectors need a paid Claude plan; on Team and Enterprise plans an owner adds the connector for the organization.

1. Open **Settings**, then **Connectors**, then **Add custom connector**.
2. Name: `Dataporium`. Remote MCP server URL: the address below, which contains your API key.
3. Click **Add**. In a chat, open the tools menu (the plus or sliders icon) and turn Dataporium on.
4. Ask a question, for example "Compare the housing market in Austin and Dallas using Dataporium".

```
https://mcp.dataporium.io/mcp?apikey=YOUR_API_KEY
```

## ChatGPT

ChatGPT Plus, Pro, Business and Enterprise support custom MCP connectors through Developer mode.

1. Open **Settings**, then **Apps & Connectors**, then **Advanced settings**, and turn on **Developer mode**.
2. Choose **Create** (custom connector). Name: `Dataporium`. MCP server URL: the address below. Authentication: No authentication. Confirm that you trust the connector.
3. In a new chat, open the tools menu, choose Developer mode and enable the Dataporium connector.
4. Ask your question. ChatGPT calls the Dataporium tools and cites the data it used.

```
https://mcp.dataporium.io/mcp?apikey=YOUR_API_KEY
```

## Claude Code

The Claude Code terminal and desktop app accept remote MCP servers with a header, so the key stays out of the address.

1. Open a terminal and run the command below once.
2. Start Claude Code. The Dataporium tools appear automatically; type `/mcp` to check the connection.

```bash
claude mcp add --transport http dataporium https://mcp.dataporium.io/mcp --header "Authorization: Bearer YOUR_API_KEY"
```

## Cursor, VS Code and Windsurf

For editors and agents that read an `mcp.json` file: Cursor, VS Code with Copilot agent mode, Windsurf, Cline and similar.

1. Open the MCP settings of the editor. Cursor: **Settings**, then **MCP**, then **Add new global MCP server**. VS Code: the `.vscode/mcp.json` file or the **MCP: Add Server** command.
2. Paste the configuration below into the file.
3. Save the file. The editor connects and lists the Dataporium tools; enable them for the agent.

```json
{
  "mcpServers": {
    "dataporium": {
      "url": "https://mcp.dataporium.io/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

## Gemini CLI

Gemini CLI reads MCP servers from its settings file. The Gemini web and mobile apps do not accept custom MCP servers yet; use Gemini CLI or an agent framework that supports MCP.

1. Open (or create) the file `~/.gemini/settings.json` on your computer.
2. Add the configuration below, then start Gemini CLI.
3. Type `/mcp` to confirm that the Dataporium server is connected.

```json
{
  "mcpServers": {
    "dataporium": {
      "httpUrl": "https://mcp.dataporium.io/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

## Grok (xAI API)

Developers using the xAI API can attach Dataporium as a remote MCP tool in a request. The Grok consumer apps do not accept custom MCP servers yet.

1. In your xAI API request (Responses API or the xAI SDK), add a tool of type `mcp` with the Dataporium server URL.
2. Grok calls the Dataporium tools during the response and returns the results with its answer.

```python
tools=[{
  "type": "mcp",
  "server_label": "dataporium",
  "server_url": "https://mcp.dataporium.io/mcp?apikey=YOUR_API_KEY"
}]
```

## Other apps

Any MCP client that supports remote servers over HTTP (Streamable HTTP transport) works.

1. Remote HTTP client: use the server URL with an `Authorization` header (`Bearer YOUR_API_KEY`), an `X-API-Key` header, or the `?apikey=` form of the URL.
2. Local-only client: apps that can only start a local server can use the `mcp-remote` bridge. Run the command below as the server command; it forwards to the Dataporium MCP server.

```bash
npx mcp-remote https://mcp.dataporium.io/mcp --header "Authorization: Bearer YOUR_API_KEY"
```

## What the assistant can access (46 tools)

| Area | What the tools read |
|---|---|
| Companies and stocks | Company profiles, prices of stocks, ETFs and indexes, financial statements, business segments down to product and country level, SEC filings, earnings transcripts, presentations, insider trades, stock trades reported by members of Congress, short interest, federal contracts, lobbying, US patents, shareholders, options |
| Markets | Stock, forex and crypto news, gainers and losers, sector and industry performance, earnings and IPO calendars, exchange hours, commodities, FX rates, weekly futures positioning by trader type |
| Economy and energy | US economic series (GDP, CPI, jobs, mortgage rates), US energy data, healthcare market data, US drug approvals and clinical trials |
| Real estate | Four tools: search homes for sale, pending, for rent, sold or off the market; one home in full by address or ID; find and rank states, counties, metros, cities and ZIP codes; one area in full with market, property tax, crime, demographics, climate and neighborhood profile |
| Industries | US banks and credit unions, consumer complaints about financial companies, vehicle and consumer product recalls, airline on-time performance and passenger traffic, pay offered in work-visa filings |
| Healthcare providers | US hospitals, health systems, doctors and clinicians, group practices, hospital financials and quality measures, Medicare procedures, prescriptions and drug spending |
| Elections | US election results: president, Senate, House, governors, state offices and ballot measures |
| Research screeners | Rank 45,000 companies or every US city and ZIP code on dozens of metrics in one call, screen M&A deals, then drill into the best matches |

Every tool and field is described in the [API documentation](https://dataporium.tech/api-docs).

## Example questions

- Which US cities have a gross rent yield above 7% with a growing population and low crime?
- Find profitable US stocks with a forward P/E below 15, revenue growth above 10% and insider buying, then compare the top five.
- What did Nvidia report last quarter, and how does its valuation compare with the sector?
- How have mortgage rates and home values in Phoenix changed over the past year?
- Show homes in Austin, Texas under $600,000 that had a price cut in the last 7 days.
- Compare Irvine, CA and Plano, TX on crime and home value.
- Which hospitals in Texas have the most beds, and which health systems own them?
- Which companies filed layoff notices in California in the last 30 days, and how many workers were affected?

## Limits and safety

- 600 API requests per minute, and 150 tool calls per hour per key through MCP.
- Answers are capped at 100 rows per call.
- Treat a server address that contains your API key like a password. Do not share screenshots of it.
- If a key leaks, create a new key in your account settings. The old one stops working.

## MCP or the Python library?

| Use | When |
|---|---|
| MCP server | You want answers in a chat or an AI agent, and do not want to write code |
| Python library | You are building an app, a dashboard, a model or a scheduled job |

Both read the same data with the same API key.

*Data is for information only and is not investment advice.*
