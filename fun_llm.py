def test_blah(a, b):
    return a+b

def openai_extract_job_ad_sections(job_ad_content, OPENAI_API_KEY, openai_model="gpt-4o" ):
    from openai import OpenAI
    import json

    # Create openai client
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_content = """
    Your HR (human resources) specialist. User will give you job advertisement content. You need to extract content for following sections:
    * Job description. Provinding description of job responsibilities and tasks. If result of this segment is list, concatenate into one string, separated by semicolon','.
    * Technical skills. Skills required for this job possitions.If result of this segment is list, concatenate into one string, separated by semicolon','.
    * Soft skills. Non-technical skills required for this job possitions.If result of this segment is list, concatenate into one string, separated by semicolon','.

    Provide response in json format

    """

    response = client.chat.completions.create(
        model=openai_model,
        messages=[
        {
        "role": "system",
        "content": system_content
        },
        {
        "role": "user",
        "content": job_ad_content
        }
        ],
        response_format = { "type": "json_object" },
        temperature=0.5,         # Low creativity
        max_tokens=1000,          # Limit response length
    )

    return json.loads(response.choices[0].message.content)