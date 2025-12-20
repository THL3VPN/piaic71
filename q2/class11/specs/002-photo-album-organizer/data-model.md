# Data Model: Photo Album Organizer

## Entities

### Photo

Represents a single photo.

**Fields**:
- `id`: INTEGER (Primary Key)
- `album_id`: INTEGER (Foreign Key to Album)
- `path`: TEXT (Path to the photo file on the local filesystem)
- `created_at`: DATETIME

### Album

Represents a collection of photos.

**Fields**:
- `id`: INTEGER (Primary Key)
- `name`: TEXT
- `created_at`: DATETIME

## Relationships

- An `Album` can have many `Photos`.
- A `Photo` belongs to one `Album`.
