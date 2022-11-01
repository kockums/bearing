# Dependencies

This guide describes the dependencies of this repository and their purpose.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Package Dependencies](#package-dependencies)
- [Peer Dependencies](#peer-dependencies)
- [Development Dependencies](#development-dependencies)

## Package Dependencies

Package dependencies, or just regular dependencies are those packages that are needed for the
library code to run properly and so are are included as part of the library's final production bundle.

## Peer Dependencies

Peer dependencies are package dependencies that the library depends on
but are not included as part of the library's final production bundle.

Usually peer dependencies are packages that would-be users would already have or need
as part of their own applications, and hence, no need to include them as part of
the library code.


### Rhino

[Rhino](https://www.rhino3d.com/) is a 3D computer graphics and computer-aided design (CAD) application.



### Grasshopper

[Grasshopper](https://www.grasshopper3d.com/) is a graphical algorithm editor tightly integrated with Rhino 3D.

#### Grasshopper Plugins

- None


## Development Dependencies

Development dependencies are package dependencies used while developing library code
but are not part of the library's final production bundle.
