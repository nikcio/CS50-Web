# Fakeflix by Nikcio

**Disclaimer. I've only run spell checking on this document, and therefore some other documents could contain spelling errors.**

[**Watch a demo of this project here**](https://youtu.be/WOfc0G8SM0c)

## Summary
The project Fakeflix is my submission to the CS50W final project. This project takes its inspiration from Netflix but does not make an identical clone. Instead, this project features a collection of media (Movies/series) of which we store information like title, date, genre, trailer, etc. This information can be seen by users and changed by editors. The project, therefore, features a dual login system and two environments for the different users. Furthermore, the project features password recovery functionality.

## Files:
To make this project I've made two apps (webapp & accounts). Webapp is used for the main functionality of the project and accounts are used for the login system as well as the password recovery functionality.

The pages all extend a base file which can be found in `webapp\templates\`
I've described what the different pages are used for [here](readme/pages.md).

Of course, the models, url, and views files are used for the different models, urls, and views used in the two apps.

The static content in the webapp consists of a few files:

`CSS`

In the css folder we find the css used for the pages. I have 3 files from bootstrap and some I've made myself:

* editorhero (used for the hero on the editor home/series page)
* home (used to style the main items on the home/editor home/editor series pages)
* myBase (used to style the navbar, body, and footer)
* newMedia (used to style the pages used when creating and updating media)
* viewtrailer (used to style the trailer page)

`JS`

In the js folder we find one file:

* combined

This file is used on the pages with media squares (home/editor home/editor series pages)
The javascript in this file takes care of updating the information on the modal which shows details about a media item. It also handles the saving functionality the program contains where the user can save media items so it shows up on the saved page.

In the `img` folder we find the image files used in the project.

The static content in accounts consists of one file this file is:

* LoginScreen

This styles the loginscreen and registration page.

The `frontend-dev` folder contains all the files used in creating the css, js, and html pages. You are welcome to have a look but I will not fully explain how it's setup. I've used a custom gulp setup to develop the design and I used sass files to write the css.

## Complexity
As described in the assignment this project goes beyond the complexity of the previous projects. This is done by introducing these key features:

* Dual login (See more info [Here](readme/login.md))
* Mostly class-based views (See more info [Here](readme/class.md))
* Recover password (See more info [Here](readme/password.md))
* Django form validation (See more info [Here](readme/form.md))
* Save system(See more info [Here](readme/save.md))
* Dynamic modal (See more info [Here](readme/modal.md))

I believe that these features together make this project sufficiently complex. The only key feature that resembles the ones made in previous assignments is the save system which resembles that of the like system in project 4 (networking).

## Design

This project started out with a Figma design which can be seen [here](https://www.figma.com/file/IPGOmOTDHwPeVBosOItfwg/CS50W-Final).
This design was used to get an idea of how the website would look and feel.

## Packages

This project uses `Pillow` to store images.
