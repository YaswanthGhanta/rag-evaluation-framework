from rag_pipeline import run_rag_pipeline


question = "Am I allowed to work remotely?"

result = run_rag_pipeline(question)


print("\n===== PIPELINE INSPECTION =====\n")

print("QUESTION:")
print(question)

print("\nRETRIEVED POLICY:")
print(result["retrieved_policy"])

print("\nACCEPTED POLICY:")
print(result["accepted_policy"])

print("\nEXACT CONTEXT:")
print(repr(result["context"]))

print("\nSUFFICIENCY:")
print(result["sufficiency"])
