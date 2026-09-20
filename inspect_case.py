from rag_pipeline import run_rag_pipeline


question = (
    "If I have unused annual leave, can I work remotely "
    "two days per week with manager approval?"
)

result = run_rag_pipeline(question)


print("\n===== CASE INSPECTION =====")

print("\nQUESTION:")
print(question)

print("\nRETRIEVED POLICY:")
print(result["retrieved_policy"])

print("\nACCEPTED POLICY:")
print(result["accepted_policy"])

print("\nCONTEXT:")
print(result["context"])

print("\nSUFFICIENCY:")
print(result["sufficiency"])

print("\nGENERATED ANSWER:")
print(result["generated_answer"])

print("\nFIRST GROUNDEDNESS:")
print(result["groundedness"])

print("\nRETRY ANSWER:")
print(result["retry_answer"])

print("\nRETRY GROUNDEDNESS:")
print(result["retry_groundedness"])

print("\nFINAL ANSWER:")
print(result["final_answer"])
