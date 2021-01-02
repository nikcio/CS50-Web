# Project 0
[**Watch a demo of this project HERE**](https://youtu.be/JhtZfsK2wOs)

## Assignment

### Specification
Your website must meet the following requirements.

* **Pages**. Your website should have at least three pages: one for Google Search, one for Google Image Search, and one for Google Advanced Search.
    * On the Google Search page, there should be links in the upper-right of the page to go to Image Search or Advanced Search. On each of the other two pages, there should be a link in the upper-right to go back to Google Search.
* **Query Text**. On the Google Search page, the user should be able to type in a query, click “Google Search”, and be taken to the Google search results for that page.
    * Like Google’s own, your search bar should be centered with rounded corners. The search button should also be centered, and should be beneath the search bar.
* **Query Images**. On the Google Image Search page, the user should be able to type in a query, click a search button, and be taken to the Google Image search results for that page.
* **Query Advanced**. On the Google Advanced Search page, the user should be able to provide input for the following four fields (taken from Google’s own advanced search options)
    * Find pages with… “all these words:”
    * Find pages with… “this exact word or phrase:”
    * Find pages with… “any of these words:”
    * Find pages with… “none of these words:”
* **Appearance**. Like Google’s own Advanced Search page, the four options should be stacked vertically, and all of the text fields should be left aligned.
    * Consistent with Google’s own CSS, the “Advanced Search” button should be blue with white text. When the “Advanced Search” button is clicked, the user should be taken to search results page for their given query.
* **Lucky**. Add an “I’m Feeling Lucky” button to the main Google Search page. Consistent with Google’s own behavior, clicking this link should take users directly to the first Google search result for the query, bypassing the normal results page.
* **Aesthetics**. The CSS you write should match Google’s own aesthetics as best as possible.



# Gulpfile.js documentation
* Gulp version: 4.0.2
* Package version: 1.3.0
* Last updated: May 2020

## Requires:
___
* [node.js 12 or newer](https://nodejs.org/en/)

## Install gulp:
___
    npm install gulp-cli -g

## Setup:
___
### 1. Run 
    npm install
### 2. Modify [package.json](./package.json)
```
{
   "name": "Nikcios-toolset",
   .
   .
   .
   "repository": {
   "type": "git",
   "url": "git+https://github.com/AUTHOR/PROJECT_NAME.git"
   },
   .
   .
   .
   "bugs": {
      "url": "https://github.com/AUTHOR/PROJECT_NAME/issues"
   },
   "homepage": "https://github.com/AUTHOR/PROJECT_NAME#readme"
}
```
Consider changing these settings before usage.
### 3. Start using gulp
    gulp

## Features
___
* SASS formatting (minification + auto-prefix)
* JavaScript formatting (minification + concat)
* HTML style and JavaScript injecting
* Automatic browser synchronization
* Image minification
* SVG formatting (minification + concat) - Out of order
* Copy video and fonts

## How to change the file structure
___
To change the structure of the src folder or the dist folder visit the [gulp-config.js](./gulp-config.js)

Here all the paths are shown and can be changed to your liking.

## File structure in folders
___
    src
        > assets
            > img
               > 350x150.png
            > fav
               > favicon.ico
        > js
            > nav.js
        > sass
            > _nav.scss
            > _footer.scss
            > base.scss
        > html
            > index.html

    dist
        > css
        > img
        > scripts
        > svg
        > video
        index.html

## Commands
___
-  `gulp` 
   -  This is the default command and runs every command in the correct order and ends on a watch which watches all file changes and operates accordingly
-  `gulp dev`
   -  Does the same as the default command
-  `gulp svg`
   -  Runs the SVG formatting
-  `gulp clean`
   -  Cleans the dist folder
-  `gulp sassFormat`
   -  Runs the SASS formatting
-  `gulp images`
   -  Runs the image formatting
-  `gulp video`
   -  Copies videos
-  `gulp fonts`
   -  Copies fonts
-  `gulp JSFormat`
   -  Runs the JavaScript formatting
-  `gulp injectToHTML`
   -  Injects styles and JavaScripts into the HTML files
-  `gulp serve`
   -  Starts a browser-sync instance
-  `gulp watch`
   -  Starts a watch of all the files in src
-  `gulp reload`
   -  Reloads the browser-sync instance

## Change browser support
___
This tool uses [browserslists](https://github.com/browserslist/browserslist) to define browser support which can be changed form the [package.json](./package.json) file

To change the support just change the "defaults" tag under browserslist:

```
"browserslist": [
    "defaults"
  ]
```
## How to inject files
To inject a html partial just the following function after creating the file inside your partial directory:
```
<!-- inject:partial:partials/htmlfile.html -->
<!-- endinject -->
```

## How to use SASS
When using SASS you can decide which files should be copied by typing a underscore before files that should now be copied.

## Help
___
### I cannot run any commands:
    If you're getting an error saying you don't have permission to run scripts run this command in your PowerShell

* `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### I'm reinstalling an existing project and have errors:
    When reinstalling delete the `package.json-lock` and the `node_modules` folder then run `npm install`.
