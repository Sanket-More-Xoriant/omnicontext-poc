from agents.chunking_agent import ChunkingAgent

agent = ChunkingAgent()

chunks = agent.create_chunks()

print(
    f"Total Chunks: {len(chunks)}"
)

print("\nFIRST CHUNK\n")

print(chunks[0])