from integrators.notion import NotionIntegration



integrator = NotionIntegration(api_token="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")

resp = integrator.fetch_data("4391404cb6bb46f8ab26b9e9a2128658")

print(resp)