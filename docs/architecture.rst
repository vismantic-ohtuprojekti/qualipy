.. _architecture:

Project architecture
********************

The project's folder structure and architecture have been kept simple::

    .
    ├── docs
    ├── qualipy
    │   ├── data
    │   │   ├── object_extraction
    │   │   └── svm
    │   ├── filters
    │   └── utils
    ├── scripts
    └── tests
        ├── accuracy
        ├── filters
        ├── images
        └── utils

The qualipy folder contain's the project's main source code. All filter classes are housed in the qualipy/filters folder, each class having its file. The common functions shared by the filters and the data they use are kept in the qualipy/utils and qualipy/data folders, respectively. For example, the commonly used SVM class can be found in the utils folder.

The qualipy.process module exploits the used structure by getting the list of available filters by inspecting the qualipy.filters package, thus being able to map the names' of the filters to their matching class objects. The process function works by calling the predict function of each of the specified class objects.

All test files, found in tests/, follow the same folder structure as the module they are testing. Additional scripts useful for creating and documenting filters can be found in the scripts/ folder in the project's root directory.
