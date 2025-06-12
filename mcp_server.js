// mcp_server.js
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios from "axios";
// import { z } from "zod";
// import { createAgent } from "@model-context-protocol/sdk";

console.log("Starting MCP server...");

// The address of your Python Flask API
const PYTHON_API_BASE_URL = "http://localhost:5000";

// Create an MCP server
const server = new McpServer({
  name: "clash_royale_ai",
  version: "1.0.0"
});

// Get Game State Tool
server.tool("get_game_state", {}, async () => {
  console.log("MCP Server: Calling Python API to get game state...");
  try {
    const response = await axios.get(`${PYTHON_API_BASE_URL}/get_game_state`);
    // We can stringify the JSON to return a clean text block to the LLM
    return {
      content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }]
    };
  } catch (error) {
    console.error("Error getting game state:", error.message);
    return {
      content: [{ type: "text", text: "Error: Could not retrieve game state from the Python server." }]
    };
  }
});
// Place Card Tool
server.tool("place_card_at_xy",
  {
    cardName: z.string().describe("The name of the card to play from your current hand. Must be an exact match."),
    x: z.number().describe("The x-coordinate (horizontal position) on the game board to place the card."),
    y: z.number().describe("The y-coordinate (vertical position) on the game board to place the card."),
    thought: z.string().describe("Your reasoning for making this specific move at this location.")
  },
  async ({ cardName, x, y, thought }) => {
    console.log(`MCP Server: Received instruction to place ${cardName} at (${x},${y}). Reason: ${thought}`);
    try {
      const response = await axios.post(`${PYTHON_API_BASE_URL}/place_card`, {
        card_name: cardName,
        x: x,
        y: y,
      });
      return {
        content: [{ type: "text", text: `Action successful: ${response.data.message}` }]
      };
    } catch (error) {
      console.error("Error placing card:", error.message);
      return {
        content: [{ type: "text", text: "Error: The card placement action failed." }]
      };
    }
  }
);


// Add an addition tool
server.tool("special_Pi_number_of_the_day",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(314) }]
  })
);

// Start receiving messages on stdin and sending messages on stdout
const transport = new StdioServerTransport();
await server.connect(transport);




// // --- 1. Define Tool Schemas with Zod ---
// // These schemas describe the tools to the LLM. The descriptions are very important!

// const getGameStateTool = z.object({}).describe(
//   "Get the current, complete state of the game, including hand, troops on board, tower health, and time remaining. This should be your first action in every turn to see what is happening."
// );

// const placeCardTool = z
//   .object({
//     cardName: z
//       .string()
//       .describe("The name of the card to play from your current hand. Must be an exact match."),
//     x: z.number().describe("The x-coordinate (horizontal position) on the game board to place the card."),
//     y: z.number().describe("The y-coordinate (vertical position) on the game board to place the card."),
//     thought: z.string().describe("Your reasoning for making this specific move at this location.")
//   })
//   .describe("Executes a game action by placing a card at a specific (x, y) coordinate on the board.");

// // --- 2. Implement the Tool Functions ---
// // These functions are what actually run when the LLM decides to use a tool.

// const tools = {
//   get_game_state: {
//     schema: getGameStateTool,
//     fn: async () => {
//       console.log("MCP Server: Calling Python API to get game state...");
//       try {
//         const response = await axios.get(`${PYTHON_API_BASE_URL}/get_game_state`);
//         // We can stringify the JSON to return a clean text block to the LLM
//         return JSON.stringify(response.data, null, 2);
//       } catch (error) {
//         console.error("Error getting game state:", error.message);
//         return "Error: Could not retrieve game state from the Python server.";
//       }
//     },
//   },
//   place_card_at_xy: {
//     schema: placeCardTool,
//     fn: async ({ cardName, x, y, thought }) => {
//       console.log(`MCP Server: Received instruction to place ${cardName} at (${x},${y}). Reason: ${thought}`);
//       try {
//         const response = await axios.post(`${PYTHON_API_BASE_URL}/place_card`, {
//           card_name: cardName,
//           x: x,
//           y: y,
//         });
//         return `Action successful: ${response.data.message}`;
//       } catch (error) {
//         console.error("Error placing card:", error.message);
//         return "Error: The card placement action failed.";
//       }
//     },
//   },
// };

// // --- 3. Create the Agent ---

// const agent = createAgent({
//   model: "gemma:2b", // Or "qwen:latest", etc. Make sure it's running in Ollama
//   ollama: true, // Use this flag for Ollama
//   tools,
// });

// // --- 4. The Main Game Loop ---

// async function gameLoop() {
//   console.log("--- Starting Clash Royale AI Agent ---");
  
//   // The System Prompt: This is where you give the LLM its instructions and persona.
//   const systemPrompt = `
//     You are a world-class, strategic Clash Royale professional player. Your goal is to win the game by destroying more of the opponent's towers than they destroy of yours.

//     Today is ${new Date().toLocaleDateString('en-ZA', { timeZone: 'Africa/Johannesburg' })}.

//     You will play the game by calling a sequence of tools. In each turn, you MUST follow this sequence:
//     1.  Call the \`get_game_state\` tool to see the board, your hand, and tower health.
//     2.  Analyze the game state carefully. Consider your elixir, the opponent's troops, their positions, and their likely next moves. Formulate a plan.
//     3.  If you decide to play a card, call the \`place_card_at_xy\` tool with the card's name, target coordinates, and your detailed reasoning in the 'thought' parameter.
//     4.  If you decide not to play a card and wait for more elixir, state "Waiting for more elixir." and explain why.

//     Think step-by-step. Your strategy should be defensive but opportunistic. Protect your towers, and then build a counter-push.
//     The game board coordinates range roughly from x=0-500 and y=0-900.
//     Let's begin the match. What is your first move?
//   `;

//   let conversation = [{ role: "system", content: systemPrompt }];

//   // Run for a limited number of turns for this example
//   for (let turn = 1; turn <= 10; turn++) {
//     console.log(`\n--- Turn ${turn} ---`);

//     const response = await agent.run(conversation);
    
//     // Add the AI's response to the conversation history
//     conversation.push(response);
    
//     console.log("AI Response:", response);

//     // If the AI made a move, there's a natural delay. If not, wait a bit.
//     await new Promise(resolve => setTimeout(resolve, 3000)); // Wait 3 seconds between turns
//   }

//   console.log("--- Game Loop Finished ---");
// }

// gameLoop().catch(console.error);
