# quickmod-json-schema
Json schema for quickmod

## Introduction
A QuickMod file is a JSON file that contains metadata about a mod for the sandbox game Minecraft. This metadata can be things like name, description, authors, different URLs (website, issue tracker, donations etc.), but also machine readable information about how to install the mod.

(Copied from [Quickmod website](http://blog.02jandal.xyz/QuickModDoc/index.html))

Json schema is a schema that is used for validating the structure of JSON data.

This repo combines this two things together and make QuickMod development easier.

## Usage
Different languages have their own implementation of json schema validation. Google your preferred language with 'json schema' will do.

## Files
A JSON does not support comments, here are the files representing.

index.json -- According to [Spec](http://blog.02jandal.xyz/QuickModDoc/qm_index_spec.html), the index quickmod file

main.json -- Main quickmod file. Including version and such
