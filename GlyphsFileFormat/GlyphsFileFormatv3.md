# Glyphs File Format, Version 3

## File Format Flavors

There are two flavors of the Glyphs file format.

### Single File (.glyphs)

A single file which contains all the data of a font source.

### Package (.glyphspackage)

The package format is the same as the single file format, but the data is split into multiple files.
This format uses a bundle structure, where a directory ending in `.glyphspackage` is presented by macOS as a regular file.
Step inside such a bundle by choosing “Show Package Contents” from the context menu in Finder.
Inside this directory, there are the following files:

- `fontinfo.plist` – The main file containing the font data.
- `order.plist` – A file containing the glyph names in their order. An array of strings.
- `UIState.plist` – A file containing the display strings. A dictionary with a `displayStrings` key following the [`displayStrings` schema](#spec-glyphs-3-displayStrings).
- `glyphs/*.glyph` – Individual files for each glyph. The files follow the [`glyph` schema](#spec-glyphs-3-glyph).

Glyphs saves its source files in a plain-text format.
This way, files can be viewed and edited in any text editor.

## File Format Details

- The file format is based on OpenStep Property Lists (also known as NeXTSTEP, ASCII, or old-style Property Lists).
- This format can be converted to JSON for validation against a JSON Schema.
- The file contents are UTF-8 encoded.
- In addition to the four core data types (dictionary, array, string, and data), Glyphs uses unquoted strings to represent numbers (integers, floats, and booleans).
  Booleans are encoded as `1` (true) and `0` (false). 
  Strings that look like numbers are always encoded in quotes.
- Whitespace is restricted to ASCII spaces, line feeds, and horizontal tabs.
- No comments (like `// ...` or `/* .... */`) are present.
- No indentation is used to reduce file size.
- Dictionaries and arrays are generally broken onto lines such that each key or element starts on a new line.
  When empty, they span two lines, one for the opening and one for the closing bracket.
- Some arrays are encoded on a single line for better readability and to reduce file size.
  These are mostly arrays used as tuples like points with X/Y coordinates.
  The `glyphsCompact` attribute in the JSON Schema indicates that the array is encoded on a single line.
- Dictionary keys are sorted alphabetically.
- Some string values do not escape horizontal tab and line feed characters, instead using the literal characters.
  This improves readability.
- Several values cannot be edited in isolation, as they are interdependent.
  For example, changing the order of elements in a list may require matching changes in other parts of the file.
- Empty dictionaries and arrays are generally omitted, except for values of a `userData` property where the structure is preserved.

## Syntax

The following Backus–Naur form describes the syntax of the Glyphs file format.

```xml
<document>       ::= <ws> <value> <ws>;
<ws>             ::= ( ' ' | '\t' | '\n' )*;
<value>          ::= <dictionary> | <array> | <string> | <number> | <data>;
<dictionary>     ::= '{' <ws> ( <key-value-pair> <ws> )* '}';
<key-value-pair> ::= <key> <ws> '=' <ws> <value> ';';
<array>          ::= '(' <ws> [ <array-elements> <ws> ] ')';
<array-elements> ::= <value> [ <ws> ',' ]
                   | <value> <ws> ',' <ws> <array-elements>;
<string>         ::= <string-quoted> | <string-bare>;
<string-quoted>  ::= '"' ( '\' <escape-sequece> | <quoted-char> )* '"';
<escape-sequece> ::= '\' | 'a' | 'b' | 'e' | 'f' | 'n' | 'r' | 't' | 'v' | '\n'
                   | <base8> [ <base8> [ <base8> ] ]
                   | 'U' <base16> <base16> <base16> <base16>;
<base8>          ::= '0'-'7';
<base16>         ::= '0'-'9' | 'A'-'F' | 'a'-'f';
<quoted-char>    ::= { any character except '"' and '' };
<string-bare>    ::= <unquoted-start> ( <unquoted-char> )*;
<unquoted-start> ::= '$' | '+' | '.' | '/' | ':' | 'A'-'Z' | '_' | 'a'-'z';
<unquoted-char>  ::= <unquoted-start> | '-' | '0'-'9';
<number>         ::= [ '-' ] ( '0'-'9' )+ [ '.' ( '0'-'9' )+ ];
<data>           ::= '<' <ws> [ <data-content> <ws> ] '>';
<data-content>   ::= <data-byte> [ <ws> <data-byte> ]*;
<data-byte>      ::= <base16> <ws> <base16>;
```

## Schema

Use the following JSON schemas to validate files.

- [glyphs-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-3.schema.json)
- [glyphs-autosave-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/glyphs-autosave-3.schema.json)
- [fontinfo-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/fontinfo-3.schema.json)
- [fontinfo-autosave-3.schema.json](https://github.com/schriftgestalt/GlyphsSDK/blob/Glyphs3/GlyphsFileFormat/Schemas/fontinfo-autosave-3.schema.json)

## Document

- <code><strong>.appVersion</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The build number of Glyphs used to save the file. Example: `"3210"`.
- <code><strong>.formatVersion</strong>: integer</code> ![required](https://img.shields.io/badge/required-204d7e) ![new](https://img.shields.io/badge/new-1c6d37) – The version of the file format. Set to `4` for version 4 or `3` for version 3. If unset, the file is considered to be version 1 as used by Glyphs 1 and Glyphs 2.
    - Possible values: `3`.
- <code><strong>DisplayStrings</strong>: array = []</code> – The strings of the Edit View tabs. Omitted when the `Write DisplayStrings` custom parameter is set to false. Omitted and written as `displayStrings` to `UIState.plist` in case of a package file. See [`displayStrings`](#spec-glyphs-3-displayStrings).
- <code><strong>axes</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The designspace variation axes of the font.
    - <code><strong>#n</strong>: object</code> See [`axis`](#spec-glyphs-3-axis).
- <code><strong>classes</strong>: array = []</code> – The OpenType layout classes of the font.
    - <code><strong>#n</strong>: object</code> See [`class`](#spec-glyphs-3-class).
- <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the font.
    - <code><strong>#n</strong>: object</code> See [`customParameter`](#spec-glyphs-3-customParameter).
- <code><strong>date</strong>: string</code> – The moment in time that is used as the creation date of exported font files including date, time, and timezone. Example: `"2024-07-17 03:14:15 +0000"`.
- <code><strong>familyName</strong>: string</code> – The font family name. Corresponds to the default value of the `familyNames` property.
- <code><strong>featurePrefixes</strong>: array = []</code> – The OpenType layout feature prefixes of the font.
    - <code><strong>#n</strong>: object</code> See [`featurePrefix`](#spec-glyphs-3-featurePrefix).
- <code><strong>features</strong>: array = []</code> – The OpenType layout features of the font.
    - <code><strong>#n</strong>: object</code> See [`feature`](#spec-glyphs-3-feature).
- <code><strong>fontMaster</strong>: array</code> ![required](https://img.shields.io/badge/required-204d7e) – The masters of the font.
 – Array (min count: 1).
    - <code><strong>#n</strong>: object</code> See [`fontMaster`](#spec-glyphs-3-fontMaster).
- <code><strong>glyphs</strong>: array</code> ![required](https://img.shields.io/badge/required-204d7e) – The glyphs of the font. The order is used on export unless the `glyphOrder` custom parameter is set.
    - <code><strong>#n</strong>: object</code> See [`glyph`](#spec-glyphs-3-glyph).
- <code><strong>instances</strong>: array = []</code> – The instances of the font.
    - <code><strong>#n</strong>: object</code> See [`instance`](#spec-glyphs-3-instance).
- <code><strong>kerningLTR</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – The left-to-right kerning of the font. See [`kerning`](#spec-glyphs-3-kerning).
- <code><strong>kerningRTL</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – The right-to-left kerning of the font. See [`kerning`](#spec-glyphs-3-kerning).
- <code><strong>kerningVertical</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – The vertical kerning of the font. See [`kerning`](#spec-glyphs-3-kerning).
- <code><strong>metrics</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The metrics of the font.
    - <code><strong>#n</strong>: object</code> See [`metric`](#spec-glyphs-3-metric).
- <code><strong>note</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The note about the font.
- <code><strong>numbers</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The numbers of the font.
    - <code><strong>#n</strong>: object</code> See [`metric`](#spec-glyphs-3-metric).
- <code><strong>properties</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The properties of the font.
    - <code><strong>#n</strong></code> See [`infoProperty`](#spec-glyphs-3-infoProperty).
- <code><strong>settings</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37)
    - <code><strong>disablesAutomaticAlignment</strong>: integer = false</code> (`bool`) – Whether automatic alignment of components is disabled.
        - Possible values: `0`, `1`.
    - <code><strong>disablesNiceNames</strong>: integer = false</code> (`bool`) – Whether to use production names instead of nice names.
        - Possible values: `0`, `1`.
    - <code><strong>gridLength</strong>: integer = 1</code> (`u32`) – The main grid length.
    - <code><strong>gridSubDivision</strong>: integer = 1</code> (`u32`) – The grid sub-division size.
    - <code><strong>keepAlternatesTogether</strong>: integer = false</code> (`bool`) – Whether to keep alternates glyphs together in Font View.
        - Possible values: `0`, `1`.
    - <code><strong>keyboardIncrement</strong>: number = 1</code> (`f32`) – The standard keyboard increment.
    - <code><strong>keyboardIncrementBig</strong>: number = 10</code> (`f32`) – The keyboard increment when holding the Shift key.
    - <code><strong>keyboardIncrementHuge</strong>: number = 100</code> (`f32`) – The keyboard increment when holding both the Shift and Command key.
    - <code><strong>previewRemoveOverlap</strong>: integer = false</code> (`bool`) – Whether to preview the effect of the Remove Overlaps filter in Edit View.
        - Possible values: `0`, `1`.
    - <code><strong>snapToObjects</strong>: integer = false</code> (`bool`) – Whether snapping is enabled in Edit View.
        - Possible values: `0`, `1`.
    - <code><strong>fontType</strong>: string = "default"</code> – The type of the font.
        - Possible values: `"default"`, `"variable"`, `"layerFont"`, `"iconSet"`.
- <code><strong>stems</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The stems of the font.
    - <code><strong>#n</strong>: object</code> See [`metric`](#spec-glyphs-3-metric).
- <code><strong>unitsPerEm</strong>: integer</code> (`u32`) ![required](https://img.shields.io/badge/required-204d7e) – The number of coordinate units on the em square.
- <code><strong>userData</strong>: object = {}</code> – Custom data associated with the font. See [`userData`](#spec-glyphs-3-userData).
- <code><strong>versionMajor</strong>: integer</code> (`u32`) ![required](https://img.shields.io/badge/required-204d7e) – The major version number of the font.
- <code><strong>versionMinor</strong>: integer</code> (`u32`) ![required](https://img.shields.io/badge/required-204d7e) – The minor version number of the font.
## Definitions

- <a name="spec-glyphs-3-anchor"></a><code><strong>anchor</strong>: object</code> – (`GSAnchor`)
    - <code><strong>locked</strong>: integer = false</code> (`bool`) ![new](https://img.shields.io/badge/new-1c6d37) – Whether the anchor is locked.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The name of the anchor.
    - <code><strong>orientation</strong>: string = "left"</code> ![new](https://img.shields.io/badge/new-1c6d37) – The orientation of the anchor. See [`orientation`](#spec-glyphs-3-orientation).
        - Possible values: `"left"`, `"center"`, `"right"`.
    - <code><strong>pos</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The position of the anchor. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>userData</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – Custom data associated with the anchor. See [`userData`](#spec-glyphs-3-userData).
- <a name="spec-glyphs-3-annotation"></a><code><strong>annotation</strong>: object</code> – (`GSAnnotation`)
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle of the annotation in degrees clockwise.
    - <code><strong>pos</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The position of the annotation. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>text</strong>: string = ""</code> – The text of an text-type annotation.
    - <code><strong>type</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The type of the annotation.
        - Possible values: `"Text"`, `"Arrow"`, `"Circle"`, `"Plus"`, `"Minus"`.
    - <code><strong>width</strong>: number = 0</code> (`f64`) – The width of an text- or circle-type annotation.
- <a name="spec-glyphs-3-attr"></a><code><strong>attr</strong>: object</code>
- <a name="spec-glyphs-3-attrShape"></a><code><strong>attrShape</strong>: object</code>
- <a name="spec-glyphs-3-axis"></a><code><strong>axis</strong>: object</code> – (`GSAxis`)
    - <code><strong>default</strong>: number = 0</code> (`f64`) – The default location on the axis.
    - <code><strong>hidden</strong>: integer = false</code> (`bool`) – Whether the axis is considered to be hidden from the font user.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string = ""</code> – The user-facing name of the axis.
    - <code><strong>tag</strong>: string = ""</code> – The OpenType tag of the axis. Must be unique within the font. The tag may be longer than four characters in which case only the first four characters are considered to be the canonical tag of the axis and the rest is used as a differentiating identifier. On export, the canonical tag is used. Multiple axes with the same canonical tag are useful for higher-order interpolation.
- <a name="spec-glyphs-3-class"></a><code><strong>class</strong>: object</code> – (`GSClass`)
    - <code><strong>automatic</strong>: integer = false</code> (`bool`) – Whether the code of the class is generated automatically.
        - Possible values: `0`, `1`.
    - <code><strong>code</strong>: string = ""</code> – The code of the class. Note that this code may not just be a whitespace-separated list of glyph names but may also contain comments and other feature code constructs. Examples: `"A B C"`, `"noon-ar noon-ar.fina noon-ar.medi noon-ar.init # noon-ar glyphs"`.
    - <code><strong>disabled</strong>: integer = false</code> (`bool`) – Whether the class is disabled.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The name of the class. The leading at sign (`@`) is not included. Examples: `"Uppercase"`, `"CombiningTopAccents"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the class.
- <a name="spec-glyphs-3-color"></a><code><strong>color</strong></code> One of 3 options.
    - Option. `array` – An RGB color with an alpha channel in the sRGB IEC61966-2.1 color space.
 – Tuple (4 items).
        - <code><strong>#0</strong>: integer</code> (`u8`) – The red color component.
        - <code><strong>#1</strong>: integer</code> (`u8`) – The green color component.
        - <code><strong>#2</strong>: integer</code> (`u8`) – The blue color component.
        - <code><strong>#3</strong>: integer</code> (`u8`) – The alpha color component.
    - Option. `array` ![new](https://img.shields.io/badge/new-1c6d37) – A gray color with an alpha channel in a perceptual generic gray color space with γ = 2.2.
 – Tuple (2 items).
        - <code><strong>#0</strong>: integer</code> (`u8`) – The gray value from `0` (black) to `255` (white).
        - <code><strong>#1</strong>: integer</code> (`u8`) – The alpha color component.
    - Option. `array` ![new](https://img.shields.io/badge/new-1c6d37) – A CMYK color with an alpha channel. The color space is device-dependent.
 – Tuple (5 items).
        - <code><strong>#0</strong>: integer</code> (`u8`) – The cyan color component.
        - <code><strong>#1</strong>: integer</code> (`u8`) – The magenta color component.
        - <code><strong>#2</strong>: integer</code> (`u8`) – The yellow color component.
        - <code><strong>#3</strong>: integer</code> (`u8`) – The black color component.
        - <code><strong>#4</strong>: integer</code> (`u8`) – The alpha color component.
- <a name="spec-glyphs-3-colorLabel"></a><code><strong>colorLabel</strong></code> One of 2 options.
    - Option. `integer` (`u8`) – The index of the color label. See also [the handbook entry on color labels](https://handbook.glyphsapp.com/glyph/#glyph/color-label).
    - Option. See [`color`](#spec-glyphs-3-color).
- <a name="spec-glyphs-3-component"></a><code><strong>component</strong>: object</code> – (`GSComponent`)
    - <code><strong>alignment</strong>: integer = 0</code> (`i8`) – (`GSComponentAlignment`) – Controls the automatic alignment of the component.
        - Possible values: `-2`, `-1`, `0`, `1`, `2`, `3`.
    - <code><strong>anchor</strong>: string</code> – The name of the attachment anchor. Set to specify a specific anchor when there are multiple candidates.
    - <code><strong>angle</strong>: number = 0</code> (`f64`) ![new](https://img.shields.io/badge/new-1c6d37) – The rotation angle of the component in degrees clockwise.
    - <code><strong>attr</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – The attributes of the component. See [`attrShape`](#spec-glyphs-3-attrShape).
    - <code><strong>keepWeight</strong>: number = 0</code> (`f64`)
    - <code><strong>locked</strong>: integer = false</code> (`bool`) – Whether the component is locked.
        - Possible values: `0`, `1`.
    - <code><strong>masterId</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The ID of the master from which the component is derived.
    - <code><strong>orientation</strong>: integer = 0</code> (`i8`) ![new](https://img.shields.io/badge/new-1c6d37) – (`GSElementOrientation`) – The orientation of the component.
        - Possible values: `0`, `1`, `2`.
    - <code><strong>piece</strong>: object = {}</code> – The Smart Component settings of the component, mapping property names to values.
        - <code>&lt;key&gt;: number</code> (`f64`)
    - <code><strong>pos</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The position (translation transform) of the component. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>ref</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) ![new](https://img.shields.io/badge/new-1c6d37) – The name of the referenced glyph.
    - <code><strong>scale</strong>: array = [1, 1]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The scale transform of the component. See [`scale`](#spec-glyphs-3-scale).
    - <code><strong>slant</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The slant transform of the component. See [`slant`](#spec-glyphs-3-slant).
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the component. See `attr` for current format versions. See [`userData`](#spec-glyphs-3-userData).
- <a name="spec-glyphs-3-customParameter"></a><code><strong>customParameter</strong>: object</code> – (`GSCustomParameter`)
    - <code><strong>disabled</strong>: integer = false</code> (`bool`) – Whether the custom parameter is disabled.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The name of the custom parameter.
    - <code><strong>value</strong></code> ![required](https://img.shields.io/badge/required-204d7e) – The value of the custom parameter.
- <a name="spec-glyphs-3-displayStrings"></a><code><strong>displayStrings</strong>: array</code>
    - <code><strong>#n</strong>: string</code>
- <a name="spec-glyphs-3-featurePrefix"></a><code><strong>featurePrefix</strong>: object</code> – (`GSFeaturePrefix`)
    - <code><strong>automatic</strong>: integer = false</code> (`bool`) – Whether the code of the feature prefix is generated automatically.
        - Possible values: `0`, `1`.
    - <code><strong>code</strong>: string = ""</code> – The code of the feature prefix. Example: `"languagesystem DFLT dflt;"`.
    - <code><strong>disabled</strong>: integer = false</code> (`bool`) – Whether the feature prefix is disabled.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The name of the feature prefix. Example: `"Languagesystems"`.
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature prefix.
- <a name="spec-glyphs-3-feature"></a><code><strong>feature</strong>: object</code> – (`GSFeature`)
    - <code><strong>automatic</strong>: integer = false</code> (`bool`) – Whether the code of the feature is generated automatically.
        - Possible values: `0`, `1`.
    - <code><strong>code</strong>: string = ""</code> ![required](https://img.shields.io/badge/required-204d7e) – The code of the feature. Example: `"sub a by a.alt;"`.
    - <code><strong>disabled</strong>: integer = false</code> (`bool`) – Whether the feature is disabled.
        - Possible values: `0`, `1`.
    - <code><strong>labels</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The labels of the feature.
        - <code><strong>#n</strong>: object</code> See [`infoValue`](#spec-glyphs-3-infoValue).
    - <code><strong>notes</strong>: string = ""</code> – A string serving as a description or comment about the feature.
    - <code><strong>tag</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) ![new](https://img.shields.io/badge/new-1c6d37) – The four-letter tag of the feature. Example: `"calt"`.
- <a name="spec-glyphs-3-fontMaster"></a><code><strong>fontMaster</strong>: object</code> – (`GSFontMaster`)
    - <code><strong>active</strong>: integer = true</code> (`bool`) – Whether the master is active.
        - Possible values: `0`, `1`.
    - <code><strong>axesValues</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The designspace location of the master.
        - <code><strong>#n</strong>: number</code> (`f64`)
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the master.
        - <code><strong>#n</strong>: object</code> See [`customParameter`](#spec-glyphs-3-customParameter).
    - <code><strong>guides</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The global guides of the master.
        - <code><strong>#n</strong>: object</code> See [`guide`](#spec-glyphs-3-guide).
    - <code><strong>iconName</strong>: string = "Regular"</code> – The name of the icon that represents the master. Generally omitted when equal to `Regular`, or equal to the default icon name of the master (`GSFontMaster.defaultIconName`).
    - <code><strong>id</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The unique identifier of the master.
    - <code><strong>metricValues</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The metric values of the master.
        - <code><strong>#n</strong>: object</code>
            - <code><strong>over</strong>: number</code> (`f64`) – The overshoot of the metric value.
            - <code><strong>pos</strong>: number</code> (`f64`) – The offset from the baseline of the metric value.
    - <code><strong>name</strong>: string</code> – The name of the master. May be omitted in file format version 1 when equal to `Regular` or the default master name.
    - <code><strong>numberValues</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The number values of the master.
        - <code><strong>#n</strong>: number</code> (`f64`)
    - <code><strong>properties</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The properties of the master.
        - <code><strong>#n</strong></code> See [`infoProperty`](#spec-glyphs-3-infoProperty).
    - <code><strong>stemValues</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The stem values of the master.
        - <code><strong>#n</strong>: number</code> (`f64`)
    - <code><strong>tempData</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – Auto-save files only: Temporary data associated with the master. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the master. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>visible</strong>: integer = true</code> (`bool`) – Whether the master is visible in the preview.
        - Possible values: `0`, `1`.
- <a name="spec-glyphs-3-glyph"></a><code><strong>glyph</strong>: object</code> – (`GSGlyph`)
    - <code><strong>case</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The case of the glyph. If unset, then the case is based on a glyph data lookup based on the glyph name.
        - Possible values: `"noCase"`, `"upper"`, `"lower"`, `"smallCaps"`, `"minor"`, `"other"`.
    - <code><strong>category</strong>: string</code> – The category of the glyph. If unset, then the category is based on a glyph data lookup based on the glyph name.
    - <code><strong>color</strong></code> – The color label of the glyph. See [`colorLabel`](#spec-glyphs-3-colorLabel).
    - <code><strong>direction</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The writing direction of the glyph. If unset, then the writing direction is based on a glyph data lookup based on the glyph name.
        - Possible values: `"BIDI"`, `"LTR"`, `"RTL"`, `"VTR"`, `"VTL"`.
    - <code><strong>export</strong>: integer = true</code> (`bool`) – Whether the glyph is exported.
        - Possible values: `0`, `1`.
    - <code><strong>glyphname</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The name of the glyph.
    - <code><strong>kernBottom</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The kerning group of the bottom side of the glyph.
    - <code><strong>kernLeft</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The kerning group of the left side of the glyph.
    - <code><strong>kernRight</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The kerning group of the right side of the glyph.
    - <code><strong>kernTop</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The kerning group of the top side of the glyph.
    - <code><strong>lastChange</strong>: string</code> – The date and time of the last change of the glyph. Example: `"2023-02-25 14:46:49 +0000"`.
    - <code><strong>layers</strong>: array</code> – The layers of the glyph.
        - <code><strong>#n</strong>: object</code> See [`layer`](#spec-glyphs-3-layer).
    - <code><strong>locked</strong>: integer = false</code> (`bool`) – Whether the glyph is locked.
        - Possible values: `0`, `1`.
    - <code><strong>metricBottom</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The bottom metrics key of the glyph.
    - <code><strong>metricLeft</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The left metrics key of the glyph.
    - <code><strong>metricRight</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The right metrics key of the glyph.
    - <code><strong>metricTop</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The top metrics key of the glyph.
    - <code><strong>metricVertOrigin</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The vertical origin metrics key of the glyph.
    - <code><strong>metricVertWidth</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The vertical width metrics key of the glyph.
    - <code><strong>metricWidth</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The width metrics key of the glyph.
    - <code><strong>note</strong>: string = ""</code> – A string serving as a description or comment about the glyph.
    - <code><strong>partsSettings</strong>: array = []</code> – A list of the Smart Glyph properties and their top/bottom values.
        - <code><strong>#n</strong>: object</code> See [`partProperty`](#spec-glyphs-3-partProperty).
    - <code><strong>production</strong>: string</code> – The production name of the glyph. If unset, then the production name is based on a glyph data lookup based on the glyph name or the Unicode code point.
    - <code><strong>script</strong>: string</code> – The script of the glyph. If unset, then the script is based on a glyph data lookup based on the glyph name.
    - <code><strong>sortName</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The sort name of the glyph. If unset, then the sort name is based on a glyph data lookup based on the glyph name.
    - <code><strong>sortNameKeep</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The sort name of the glyph used in the *Keep Alternates Next to Base Glyph* display mode. If unset, then the sort name is based on a glyph data lookup based on the glyph name.
    - <code><strong>subCategory</strong>: string</code> – The subcategory of the glyph. If unset, then the subcategory is based on a glyph data lookup based on the glyph name.
    - <code><strong>tags</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The tags of the glyph, sorted lexicographically.
        - <code><strong>#n</strong>: string</code>
    - <code><strong>unicode</strong></code> – The Unicode code points of the glyph. One of 2 options.
        - Option. `integer` (`u32`) ![new](https://img.shields.io/badge/new-1c6d37) – The code point value. Examples: `65`, `125184`, `0`.
        - Option. `array` ![new](https://img.shields.io/badge/new-1c6d37) – A ascending list of code point values.
 – Array (min count: 2).
            - <code><strong>#n</strong>: integer</code> (`u32`) Examples: `65`, `125184`, `0`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the glyph. See [`userData`](#spec-glyphs-3-userData).
- <a name="spec-glyphs-3-guide"></a><code><strong>guide</strong>: object</code> – (`GSGuide`)
    - <code><strong>angle</strong>: number = 0</code> (`f64`) – The angle at which the guide is drawn in degrees clockwise.
    - <code><strong>filter</strong>: string</code> – The filter of the guide. The syntax is the description of [NSPredicate](https://developer.apple.com/documentation/foundation/nspredicate). Omitted when no filter is defined.
    - <code><strong>grid</strong>: number = 0</code> (`f64`) – The grid of the guide.
    - <code><strong>length</strong>: number = 0</code> (`f64`) – The length of a line-type guide.
    - <code><strong>lockAngle</strong>: integer = false</code> (`bool`) – Whether the angle of the guide is locked.
        - Possible values: `0`, `1`.
    - <code><strong>locked</strong>: integer = false</code> (`bool`) – Whether the guide is locked.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string = ""</code> – The name of the guide.
    - <code><strong>orientation</strong>: string = "left"</code> ![new](https://img.shields.io/badge/new-1c6d37) – The orientation of the guide. See [`orientation`](#spec-glyphs-3-orientation).
        - Possible values: `"left"`, `"center"`, `"right"`.
    - <code><strong>pos</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The position of the guide. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>showMeasurement</strong>: integer = false</code> (`bool`) – Whether the measurement of the guide is shown.
        - Possible values: `0`, `1`.
    - <code><strong>size</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The size of the guide. See [`size`](#spec-glyphs-3-size).
    - <code><strong>type</strong>: string = "Line"</code> ![new](https://img.shields.io/badge/new-1c6d37) – The type of the guide.
        - Possible values: `"Line"`, `"Circle"`, `"Rect"`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the guide. See [`userData`](#spec-glyphs-3-userData).
- <a name="spec-glyphs-3-hint"></a><code><strong>hint</strong>: object</code> – (`GSHint`)
    - <code><strong>horizontal</strong>: integer = false</code> (`bool`) – Whether the hint is horizontal. Not written for path components.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string</code> – The name of the hint.
    - <code><strong>options</strong>: number = 0</code> (`u32`) – The options of the hint.
    - <code><strong>origin</strong></code> – The origin of the hint. See [`indexPath`](#spec-glyphs-3-indexPath).
    - <code><strong>other1</strong></code> – The first other point of the hint, used by TrueType instructions that need more than two nodes. See [`indexPath`](#spec-glyphs-3-indexPath).
    - <code><strong>other2</strong></code> – The second other point of the hint, used by TrueType instructions that need more than three nodes. See [`indexPath`](#spec-glyphs-3-indexPath).
    - <code><strong>place</strong>: array</code> ![new](https://img.shields.io/badge/new-1c6d37)
 – Tuple (2 items).
        - <code><strong>#0</strong>: number</code> (`f64`) – The origin placement.
        - <code><strong>#1</strong>: number</code> (`f64`) – The width of the hint. `21` for bottom ghost hints and flex hints, `-20` for top ghost hints.
    - <code><strong>scale</strong>: array = [1, 1]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The scale of the hint. See [`scale`](#spec-glyphs-3-scale).
    - <code><strong>settings</strong>: object</code> – The settings of the hint.
    - <code><strong>stem</strong>: number</code> (`i32`) – The stem of the hint.
    - <code><strong>target</strong></code> One of 2 options.
        - Option. See [`indexPath`](#spec-glyphs-3-indexPath).
        - Option. `string` ![new](https://img.shields.io/badge/new-1c6d37) – The target of a ghost hint.
            - Possible values: `"up"`, `"down"`.
    - <code><strong>type</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) ![new](https://img.shields.io/badge/new-1c6d37) – The type of the hint.
        - Possible values: `"TopGhost"`, `"BottomGhost"`, `"Stem"`, `"Flex"`, `"TTStem"`, `"TTShift"`, `"TTSnap"`, `"TTInterpolate"`, `"TTDiagonal"`, `"TTDelta"`, `"Tag"`, `"Corner"`, `"Cap"`, `"Brush"`, `"Segment"`, `"Auto"`, `"Unknown"`.
- <a name="spec-glyphs-3-image"></a><code><strong>image</strong>: object</code> – (`GSImage`)
    - <code><strong>alpha</strong>: number = 100</code> (`f64`) – The alpha value of the image.
    - <code><strong>angle</strong>: number = 0</code> (`f64`) ![new](https://img.shields.io/badge/new-1c6d37) – The rotation angle of the image in degrees clockwise.
    - <code><strong>crop</strong>: array</code> ![new](https://img.shields.io/badge/new-1c6d37) – The cropped frame of the image, specified as the crop origin X/Y and size width/height.
 – Tuple (4 items).
        - <code><strong>#0</strong>: number</code> (`f64`) – The X coordinate of the crop origin.
        - <code><strong>#1</strong>: number</code> (`f64`) – The Y coordinate of the crop origin.
        - <code><strong>#2</strong>: number</code> (`f64`) – The width of the crop size.
        - <code><strong>#3</strong>: number</code> (`f64`) – The height of the crop size.
    - <code><strong>imagePath</strong>: string</code> – The file path of the image file relative to the document file.
    - <code><strong>imageURL</strong>: string</code> – The URL bookmark data of the image file path.
    - <code><strong>locked</strong>: integer = false</code> (`bool`) – Whether the image is locked.
        - Possible values: `0`, `1`.
    - <code><strong>pos</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The position of the image. See [`pos`](#spec-glyphs-3-pos).
    - <code><strong>scale</strong>: array = [1, 1]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The scale factor of the image. See [`scale`](#spec-glyphs-3-scale).
    - <code><strong>slant</strong>: array = [0, 0]</code> ![new](https://img.shields.io/badge/new-1c6d37) – The slant factor of the image. See [`slant`](#spec-glyphs-3-slant).
- <a name="spec-glyphs-3-instance"></a><code><strong>instance</strong>: object</code> – (`GSInstance`)
    - <code><strong>axesValues</strong>: array</code> – The internal axis locations of the instance. These values are also used for the external axis locations, if no external axis locations are specified separately.
        - <code><strong>#n</strong>: number</code> (`f64`)
    - <code><strong>customParameters</strong>: array = []</code> – The custom parameters of the instance.
        - <code><strong>#n</strong>: object</code> See [`customParameter`](#spec-glyphs-3-customParameter).
    - <code><strong>exports</strong>: integer = true</code> (`bool`) – Whether the instance is exported.
        - Possible values: `0`, `1`.
    - <code><strong>instanceInterpolations</strong>: object = {}</code> – The interpolation factors where the keys are the master IDs.
        - <code>&lt;key&gt;</code> One of 2 options.
            - Option. `number` (`f64`) – The X and Y factors are the same.
            - Option. `array` ![new](https://img.shields.io/badge/new-1c6d37) – The X and Y factors.
 – Tuple (2 items).
                - <code><strong>#0</strong>: number</code> (`f64`) – The X factor.
                - <code><strong>#1</strong>: number</code> (`f64`) – The Y factor.
    - <code><strong>isBold</strong>: integer = false</code> (`bool`) – Whether the instance is bold.
        - Possible values: `0`, `1`.
    - <code><strong>isItalic</strong>: integer = false</code> (`bool`) – Whether the instance is italic.
        - Possible values: `0`, `1`.
    - <code><strong>linkStyle</strong>: string</code> – The name of the style-linked instance.
    - <code><strong>manualInterpolation</strong>: integer = false</code> (`bool`) – Whether the `instanceInterpolations` values are used. Otherwise, the values are calculated from the axis values.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string</code> – The style name of the instance. Examples: `"Regular"`, `"Bold"`, `"Italic"`, `"Bold Italic"`.
    - <code><strong>properties</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37)
        - <code><strong>#n</strong></code> See [`infoProperty`](#spec-glyphs-3-infoProperty).
    - <code><strong>type</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The type of the instance.
        - Possible values: `"single"`, `"variable"`, `"icon"`.
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the instance. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>visible</strong>: integer = true</code> (`bool`) ![new](https://img.shields.io/badge/new-1c6d37) – Whether the instance is visible when previewing all instances.
        - Possible values: `0`, `1`.
    - <code><strong>weightClass</strong>: integer = 400</code> (`u16`) ![new](https://img.shields.io/badge/new-1c6d37) – The weight class of the instance.
    - <code><strong>widthClass</strong>: integer = 5</code> (`u16`) ![new](https://img.shields.io/badge/new-1c6d37) – The width class of the instance.
- <a name="spec-glyphs-3-indexPath"></a><code><strong>indexPath</strong></code> One of 4 options.
    - Option. `array` ![new](https://img.shields.io/badge/new-1c6d37) – The index path of a node on a path.
 – Tuple (2 items).
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape.
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node on a path.
    - Option. `array` ![new](https://img.shields.io/badge/new-1c6d37) – The index path of an inflection, where the first two path components point to an on-curve node that finishes a curve segment. The inflection component is most likely `0`.
 – Tuple (3 items).
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape.
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node on a path.
        - <code><strong>#2</strong>: number</code> (`u32`) – The index of an inflection.
    - Option. `array` ![new](https://img.shields.io/badge/new-1c6d37) – Points to the intersection of two path segments. The nodes are the ones finishing the segments.
 – Tuple (4 items).
        - <code><strong>#0</strong>: number</code> (`u32`) – The index of a path shape (P1).
        - <code><strong>#1</strong>: number</code> (`u32`) – The index of a node (N1) on P1.
        - <code><strong>#2</strong>: number</code> (`u32`) – The index of a path shape (P2).
        - <code><strong>#3</strong>: number</code> (`u32`) – The index of a node (N2) on P2.
    - Option. `string` ![new](https://img.shields.io/badge/new-1c6d37) – An attachment to the left or right side-bearing.
        - Possible values: `"lsb"`, `"rsb"`.
- <a name="spec-glyphs-3-kerning"></a><code><strong>kerning</strong>: object = {}</code> – Maps master IDs to kerning definitions.
    - <code>&lt;key&gt;: object</code> – Maps glyph names or class names to kerning partners.
        - <code>&lt;key&gt;: object</code> – Maps glyph names or class names to kerning values.
            - <code>&lt;key&gt;: number</code> (`f64`)
- <a name="spec-glyphs-3-layer"></a><code><strong>layer</strong>: object</code> – (`GSLayer`)
    - <code><strong>anchors</strong>: array = []</code> – The anchors of the layer.
        - <code><strong>#n</strong>: object</code> See [`anchor`](#spec-glyphs-3-anchor).
    - <code><strong>annotations</strong>: array = []</code> – The annotations of the layer.
        - <code><strong>#n</strong>: object</code> See [`annotation`](#spec-glyphs-3-annotation).
    - <code><strong>associatedMasterId</strong>: string</code> – The unique identifier of the associated master. Omitted when equalt to the layer ID.
    - <code><strong>attr</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – The attributes of the layer. See [`attr`](#spec-glyphs-3-attr).
    - <code><strong>background</strong>: object</code>
        - <code><strong>anchors</strong>: array = []</code> – The anchors of the background layer.
            - <code><strong>#n</strong>: object</code> See [`anchor`](#spec-glyphs-3-anchor).
        - <code><strong>annotations</strong>: array = []</code> – The annotations of the background layer.
            - <code><strong>#n</strong>: object</code> See [`annotation`](#spec-glyphs-3-annotation).
        - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-3-image).
        - <code><strong>guides</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The guides of the background layer.
            - <code><strong>#n</strong>: object</code> See [`guide`](#spec-glyphs-3-guide).
        - <code><strong>hints</strong>: array = []</code> – The hints of the background layer.
            - <code><strong>#n</strong>: object</code> See [`hint`](#spec-glyphs-3-hint).
        - <code><strong>shapes</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The shapes of the background layer.
            - <code><strong>#n</strong></code> See [`shape`](#spec-glyphs-3-shape).
    - <code><strong>backgroundImage</strong>: object</code> – The background image of the layer. See [`image`](#spec-glyphs-3-image).
    - <code><strong>color</strong></code> – The color label of the layer. See [`colorLabel`](#spec-glyphs-3-colorLabel).
    - <code><strong>guides</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The guides of the layer.
        - <code><strong>#n</strong>: object</code> See [`guide`](#spec-glyphs-3-guide).
    - <code><strong>hints</strong>: array = []</code> – The hints of the layer.
        - <code><strong>#n</strong>: object</code> See [`hint`](#spec-glyphs-3-hint).
    - <code><strong>layerId</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The unique ID of the layer. Matches the master ID when the layer is a master layer.
    - <code><strong>metricBottom</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The bottom metrics key of the layer.
    - <code><strong>metricLeft</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The left metrics key of the layer.
    - <code><strong>metricRight</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The right metrics key of the layer.
    - <code><strong>metricTop</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The top metrics key of the layer.
    - <code><strong>metricVertOrigin</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The vertical origin metrics key of the layer.
    - <code><strong>metricVertWidth</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The vertical width metrics key of the layer.
    - <code><strong>metricWidth</strong>: string</code> ![new](https://img.shields.io/badge/new-1c6d37) – The width metrics key of the layer.
    - <code><strong>name</strong>: string = ""</code> – The name of the layer. Master layers and other special layers display a name in the Glyphs UI that is derived from the layers role (for example, the name of the master that the layer belongs to). These derived names are not written to the file. Instead, this name is only displayed in the UI for non-special layers (like backup layers).
    - <code><strong>partSelection</strong>: object</code> ![new](https://img.shields.io/badge/new-1c6d37) – The Smart Glyph setting of the layer. The keys are the property names. The values are either `1` if the layer corresponds to the bottom value of the property or `2` if the layer corresponds to the top value of the property. If a layer is neither the top nor the bottom value, the property is omitted.
        - <code>&lt;key&gt;: integer</code>
            - Possible values: `1`, `2`.
    - <code><strong>shapes</strong>: array = []</code> ![new](https://img.shields.io/badge/new-1c6d37) – The shapes of the layer.
        - <code><strong>#n</strong></code> See [`shape`](#spec-glyphs-3-shape).
    - <code><strong>userData</strong>: object = {}</code> – Custom data associated with the layer. See [`userData`](#spec-glyphs-3-userData).
    - <code><strong>vertOrigin</strong>: number = 0</code> (`f64`) ![new](https://img.shields.io/badge/new-1c6d37) – The vertical origin of the layer.
    - <code><strong>vertWidth</strong>: number = 0</code> (`f64`) ![new](https://img.shields.io/badge/new-1c6d37) – The vertical width of the layer.
    - <code><strong>visible</strong>: integer = false</code> (`bool`) – Whether the layer is visible.
        - Possible values: `0`, `1`.
    - <code><strong>width</strong>: number = 0</code> (`f64`) ![required](https://img.shields.io/badge/required-204d7e) – The width of the layer.
- <a name="spec-glyphs-3-metric"></a><code><strong>metric</strong>: object</code> – (`GSMetric`)
    - <code><strong>filter</strong>: string</code> – The filter of the metric limiting the scope of the metric to a subset of glyphs.
    - <code><strong>horizontal</strong>: integer = false</code> (`bool`) – Whether the metric is a horizontal metric.
        - Possible values: `0`, `1`.
    - <code><strong>name</strong>: string</code> – The name of the metric.
    - <code><strong>type</strong>: string</code> – The type of the metric.
        - Possible values: `"ascender"`, `"cap height"`, `"slant height"`, `"x-height"`, `"midHeight"`, `"topHeight"`, `"bodyHeight"`, `"descender"`, `"baseline"`, `"italic angle"`, `"italic slope"`.
- <a name="spec-glyphs-3-node"></a><code><strong>node</strong>: array</code> – (`GSNode`)
 – Tuple (3–4 items).
    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the node.
    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the node.
    - <code><strong>#2</strong>: string</code> – The configuration of the node expressed as a sequence of characters. Types: `m`: move, `l`: line, `c`: cubic curve, `q`: quadratic curve, `o`: off-curve. Connection (may follow `l`, `c`, `q`): `s`: smooth. Orientation (left is the default): `R`: right, `C`: center. Locking (not locked is the default): `X`: locked.
    - <code><strong>#3</strong>: object = {}</code> – The attributes of the node. See [`attrShape`](#spec-glyphs-3-attrShape).
- <a name="spec-glyphs-3-infoProperty"></a><code><strong>infoProperty</strong></code> – (`GSInfoProperty`) One of 2 options.
    - Option. `object`
        - <code><strong>key</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The key of the property.
        - <code><strong>value</strong></code> ![required](https://img.shields.io/badge/required-204d7e) – The value of the property.
    - Option. `object`
        - <code><strong>key</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The key of the property.
        - <code><strong>values</strong>: array</code> ![required](https://img.shields.io/badge/required-204d7e) – The values of the property.
            - <code><strong>#n</strong>: object</code> See [`infoValue`](#spec-glyphs-3-infoValue).
- <a name="spec-glyphs-3-infoValue"></a><code><strong>infoValue</strong>: object</code> – (`GSInfoValue`)
    - <code><strong>language</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The language tag of the string value. The tag is based on the [OpenType Language System Tags](https://learn.microsoft.com/en-us/typography/opentype/spec/languagetags) but omitts trailing whitespace. Examples: `"dflt"`, `"DEU"`.
    - <code><strong>value</strong>: string</code> ![required](https://img.shields.io/badge/required-204d7e) – The localized string value.
- <a name="spec-glyphs-3-orientation"></a><code><strong>orientation</strong>: string</code> – (`GSElementOrientation`)
    - Possible values: `"left"`, `"center"`, `"right"`.
- <a name="spec-glyphs-3-partProperty"></a><code><strong>partProperty</strong>: object</code> – (`GSPartProperty`)
    - <code><strong>bottomName</strong>: string</code> – The name of the bottom value of the property. (Unused)
    - <code><strong>bottomValue</strong>: integer</code> (`i32`) – The lower end of the value range of the property.
    - <code><strong>name</strong>: string</code> – The name of the property.
    - <code><strong>topName</strong>: string</code> – The name of the top value of the property. (Unused)
    - <code><strong>topValue</strong>: integer</code> (`i32`) – The upper end of the value range of the property.
- <a name="spec-glyphs-3-path"></a><code><strong>path</strong>: object</code> – (`GSPath`)
    - <code><strong>attr</strong>: object = {}</code> ![new](https://img.shields.io/badge/new-1c6d37) – The attributes of the path. See [`attrShape`](#spec-glyphs-3-attrShape).
    - <code><strong>closed</strong>: integer</code> (`bool`) ![required](https://img.shields.io/badge/required-204d7e) – Whether the path is closed.
        - Possible values: `0`, `1`.
    - <code><strong>locked</strong>: integer = false</code> (`bool`) ![new](https://img.shields.io/badge/new-1c6d37) – Whether the path is locked.
        - Possible values: `0`, `1`.
    - <code><strong>nodes</strong>: array</code> ![required](https://img.shields.io/badge/required-204d7e) – The on- and off-curve nodes of the path.
        - <code><strong>#n</strong>: array</code> ![new](https://img.shields.io/badge/new-1c6d37) See [`node`](#spec-glyphs-3-node).
- <a name="spec-glyphs-3-pos"></a><code><strong>pos</strong>: array</code>
 – Tuple (2 items).
    - <code><strong>#0</strong>: number</code> (`f64`) – The x-coordinate of the position.
    - <code><strong>#1</strong>: number</code> (`f64`) – The y-coordinate of the position.
- <a name="spec-glyphs-3-scale"></a><code><strong>scale</strong>: array</code>
 – Tuple (2 items).
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal scale factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical scale factor.
- <a name="spec-glyphs-3-shape"></a><code><strong>shape</strong></code> – (`GSShape`) One of 2 options.
    - Option. `object` See [`path`](#spec-glyphs-3-path).
    - Option. `object` See [`component`](#spec-glyphs-3-component).
- <a name="spec-glyphs-3-size"></a><code><strong>size</strong>: array</code>
 – Tuple (2 items).
    - <code><strong>#0</strong>: number</code> (`f64`) – The width.
    - <code><strong>#1</strong>: number</code> (`f64`) – The height.
- <a name="spec-glyphs-3-slant"></a><code><strong>slant</strong>: array</code>
 – Tuple (2 items).
    - <code><strong>#0</strong>: number</code> (`f64`) – The horizontal slant factor.
    - <code><strong>#1</strong>: number</code> (`f64`) – The vertical slant factor.
- <a name="spec-glyphs-3-userData"></a><code><strong>userData</strong>: object</code>

## Changes

### 14. Jan. 2025

- Reworked JSON Schemas and added variants for package and autosave files.
- Expanded descriptions and annotations for most values.

### 1. March 2021

- add description of .glyphspackage files

### September – December 2020

- several fixes and additions
- add JSON schema for Glyphs 2 and 3 files

### 4. Jan. 2019

- First Draft for version 3

### 1. Oct. 2018:

- Add Notes about special cases
- Better general explanation

### 21. April 2018:

- Add .appVersion, disablesNiceNames, customValue, weight, width, custom
- Fix typos: paths, widthValue

### 4. Feb. 2016:

- added hints
- updated and added a few field in layers
