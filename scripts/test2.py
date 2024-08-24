import internetarchive
import os
import yaml

# Search for movies in the Internet Archive
search = internetarchive.search_items(
    #'collection:feature_films AND mediatype:movies AND mediatype:feature_films',
    'collection:feature_films AND mediatype:movies AND language:eng',
    params={'rows': 50, 'sort[]': 'downloads desc'}
)

# Store the metadata for each movie
movie_stash = []

for result in search:
    identifier = result['identifier']
    title = result.get('title', 'Untitled')
    item = internetarchive.get_item(identifier)
    metadata = item.metadata
    
    # If the title is missing or empty, assign "Untitled"
    title = metadata.get('title', 'Untitled')
    
    # Add the metadata to the stash
    movie_stash.append({
        'title': title,
        'description': metadata.get('description', 'No description available.'),
        #'embed_code': f'<iframe src="https://archive.org/embed/{identifier}" width="640" height="480" frameborder="0" allowfullscreen></iframe>',
        'video_url': f'https://archive.org/download/{identifier}/{identifier}.mp4',  # Example file path
        'download_url': f'https://archive.org/download/{identifier}/{identifier}.mp4',
        'archive_link': f'https://archive.org/details/{identifier}',
        'image_url': f'https://archive.org/download/{identifier}/{identifier}.jpg'  # Example for images if available
    })

# Write the data to a YAML file
with open('data/movies.yaml', 'w') as file:
    yaml.dump(movie_stash, file, default_flow_style=False)




