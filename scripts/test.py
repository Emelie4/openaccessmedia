#for the original markdwnfiles that I wanted to create

import internetarchive
import os

# Search for movies in the Internet Archive
search = internetarchive.search_items(
    'collection:feature_films AND mediatype:movies',
    params={'rows': 10}
)

# Store the metadata for each movie
movie_stash = []

for result in search:
    identifier = result['identifier']
    title = result.get('title', 'Untitled')
    
    item = internetarchive.get_item(identifier)
    metadata = item.metadata
    
    # Skip items without required metadata
    if 'title' not in metadata or 'description' not in metadata:
        continue
    
    # Check if the item has an .mp4 file
    item_files = item.files
    mp4_files = [file['name'] for file in item_files if file['name'].endswith('.mp4')]
    
    if mp4_files:
        # Add the metadata to the stash
        movie_stash.append({
            'title': metadata['title'],
            'description': metadata['description'],
            'video_url': f'https://archive.org/download/{identifier}/{mp4_files[0]}',  # Use the first .mp4 file found
            'download_url': f'https://archive.org/download/{identifier}/{mp4_files[0]}',
            'archive_link': f'https://archive.org/details/{identifier}'
        })

# Generate Markdown files for each movie
for movie in movie_stash:
    file_content = f"""
---
title: "{movie['title']}"
description: "{movie['description']}"
video_url: "{movie['video_url']}"
download_url: "{movie['download_url']}"
archive_link: "{movie['archive_link']}"
---

Watch the movie below:

<video controls>
    <source src="{{{{ .Params.video_url }}}}" type="video/mp4">
    Your browser does not support the video tag.
</video>

[Download Movie]({{{{ .Params.download_url }}}}) | [View on Archive.org]({{{{ .Params.archive_link }}}})
    """
    
    # Sanitize the filename
    filename = movie['title'].replace(" ", "_").replace("/", "-").lower() + '.md'
    
    # Write the file to the Hugo content directory
    with open(f'content/movies/{filename}', 'w') as file:
        file.write(file_content)
    
    print(f"Generated Markdown for {movie['title']}...")

