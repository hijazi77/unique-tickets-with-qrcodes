import asyncio
from pocketbase import PocketBase

client = PocketBase('http://127.0.0.1:8090')

async def create_multiple_records(records):
    tasks = []
    for record in records:
        task = client.collection("your_collection").create(record)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful_creations = []
    failed_creations = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Failed to create record {i+1}: {result}")
            failed_creations.append((records[i], result))
        else:
            successful_creations.append(result)
    
    return successful_creations, failed_creations

async def main():
    records_to_create = [
        {'field1': 'value1', 'field2': 'value2'},
        {'field1': 'value3', 'field2': 'value4'},
        # ... more records ...
    ]
    
    successful, failed = await create_multiple_records(records_to_create)
    
    print(f"Successfully created {len(successful)} records")
    print(f"Failed to create {len(failed)} records")

asyncio.run(main())
