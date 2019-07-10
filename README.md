# OpaquePredicatePatcher (v1.0 alpha)
Author: **Vector 35 Inc**

_Automatically patch opaque predicates_

## Description:

This script will automatically remove conditional branches which have constant conditions. It can be run from the command line via:

```python -mOpaquePredicatePatcher.__main__```

if the BinaryNinja python library is in your path. or installed as a plugin in your user plugin directory.

Read about how this tool was created on our blog: [Automated Opaque Predicate Removal](https://binary.ninja/2017/10/01/automated-opaque-predicate-removal.html)

### Example

![Before and After](opaque_predicate_elimination.gif 'Before and After')

## Minimum Version

This plugin requires the following minimum version of Binary Ninja:

 * dev - 1.0.dev-945


## Required Dependencies

The following dependencies are required for this plugin:



## License

This plugin is released under a [MIT](LICENSE) license.


