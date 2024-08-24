import internetarchive
import yaml
import os

# Define a dictionary of collection IDs and corresponding genre names
collections = {
    'SciFi_Horror': 'scifi_horror',
    'Film_Noir': 'film_noir',
    'Comedy_Films': 'comedy',
    'Silent_Films': 'silent_films'
}

# Loop through each collection and generate a YAML file
for collection_id, genre in collections.items():
    print(f"Processing collection: {genre}")
    
    # Search within the specified collection
    search = internetarchive.search_items(
        f'collection:{collection_id} AND mediatype:movies',
        params={'rows': 10}  # Adjust rows as needed
    )

    movie_stash = []
    for result in search:
        identifier = result['identifier']
        item = internetarchive.get_item(identifier)
        metadata = item.metadata

        if 'title' not in metadata or 'description' not in metadata:
            continue

        movie_stash.append({
            'title': metadata['title'],
            'description': metadata['description'],
            'video_url': f'https://archive.org/download/{identifier}/{identifier}.mp4',
            #'embed_code': f'<iframe src="https://archive.org/embed/{identifier}" width="640" height="480" frameborder="0" allowfullscreen></iframe>',
            'download_url': f'https://archive.org/download/{identifier}/{identifier}.mp4',
            'archive_link': f'https://archive.org/details/{identifier}'
        })

    # Create the YAML file for the genre
    os.makedirs('data', exist_ok=True)
    with open(f'data/{genre}.yaml', 'w') as file:
        yaml.dump(movie_stash, file)

    print(f"Finished processing {genre}.")

print("All collections processed.")

