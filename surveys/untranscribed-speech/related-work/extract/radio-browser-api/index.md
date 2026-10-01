**Source:** *Radio Browser API Reference* — [original page](https://docs.radio-browser.info/)

[ NAV 

![Figure](figures/3332a4dd4dc492578b21a922bba79453ab0aa9d9029b5b97588eac42fed78117.png)

  ](https://docs.radio-browser.info/)



![Figure](figures/b25cd9101e474c0474fc256d581eb05f395ee8c31e0f6da2570fa638d01a1446.png)

 

[json](https://docs.radio-browser.info/) [xml](https://docs.radio-browser.info/) [csv](https://docs.radio-browser.info/) [m3u](https://docs.radio-browser.info/) [pls](https://docs.radio-browser.info/) [xspf](https://docs.radio-browser.info/)



  * [Introduction](https://docs.radio-browser.info/#introduction)
  * [Using the API](https://docs.radio-browser.info/#using-the-api)
  * [Structs](https://docs.radio-browser.info/#structs)
    * [Station](https://docs.radio-browser.info/#station)
    * [Station check](https://docs.radio-browser.info/#station-check)
    * [Station check step](https://docs.radio-browser.info/#station-check-step)
  * [Lists](https://docs.radio-browser.info/#lists)
    * [List of radio stations](https://docs.radio-browser.info/#list-of-radio-stations)
    * [List of all radio stations](https://docs.radio-browser.info/#list-of-all-radio-stations)
    * [List of codecs](https://docs.radio-browser.info/#list-of-codecs)
    * [List of countries](https://docs.radio-browser.info/#list-of-countries)
    * [List of country codes](https://docs.radio-browser.info/#list-of-country-codes)
    * [List of states](https://docs.radio-browser.info/#list-of-states)
    * [List of languages](https://docs.radio-browser.info/#list-of-languages)
    * [List of tags](https://docs.radio-browser.info/#list-of-tags)
    * [List of station clicks](https://docs.radio-browser.info/#list-of-station-clicks)
    * [List of station check results](https://docs.radio-browser.info/#list-of-station-check-results)
    * [List of station check steps](https://docs.radio-browser.info/#list-of-station-check-steps)
    * [Advanced station search](https://docs.radio-browser.info/#advanced-station-search)
    * [Search radio stations by URL](https://docs.radio-browser.info/#search-radio-stations-by-url)
    * [Search radio stations by UUIDs](https://docs.radio-browser.info/#search-radio-stations-by-uuids)
    * [Server config](https://docs.radio-browser.info/#server-config)
    * [Server mirrors](https://docs.radio-browser.info/#server-mirrors)
    * [Prometheus monitoring](https://docs.radio-browser.info/#prometheus-monitoring)
    * [Server stats](https://docs.radio-browser.info/#server-stats)
  * [Modify](https://docs.radio-browser.info/#modify)
    * [Add radio station](https://docs.radio-browser.info/#add-radio-station)
    * [Station click counter](https://docs.radio-browser.info/#station-click-counter)
    * [Vote for a station](https://docs.radio-browser.info/#vote-for-a-station)
  * [Stations](https://docs.radio-browser.info/#stations)
    * [Broken stations](https://docs.radio-browser.info/#broken-stations)
    * [Stations by clicks](https://docs.radio-browser.info/#stations-by-clicks)
    * [Stations by recent clicks](https://docs.radio-browser.info/#stations-by-recent-clicks)
    * [Stations by recently changed](https://docs.radio-browser.info/#stations-by-recently-changed)
    * [Stations by votes](https://docs.radio-browser.info/#stations-by-votes)
    * [Old versions of stations](https://docs.radio-browser.info/#old-versions-of-stations)


  * [Fork on Github](https://github.com/segler-alex/radiobrowser-api-rust)
  * [Docs Powered by Slate](https://github.com/slatedocs/slate)



# Introduction

Server version: 

This webservice can be used freely but without guarantee to work. I have been keeping it online since December, 2015, but downtimes are possible and I am not always home to fix it :) Please do not hesitate to send me ideas to improve the service at [segler_alex AT web DOT de](mailto:segler_alex@web.de).

# Using the API

> **Format**
    
    
    GET {path}
    User-Agent: {user-agent}/{version}
    Host: {root end-point}
    Content-type: {MIME type}
    
    

> **GET request examples**
    
    
    GET /json/stations/search?tag=rock&codec=mp3&order=country&reverse=true&limit=1000
    User-Agent: Cool Radio App/1.2
    Host: https://de1.api.radio-browser.info
    Content-type: application/json; charset=utf-8
    
    
    
    
    GET /m3u/stations/bycountry/austria
    User-Agent: Cool Radio App/1.2
    Host: https://de1.api.radio-browser.info
    Content-type: text/plain
    
    

Please send a descriptive User-Agent in your HTTP requests, which makes it easier for me to get in touch with developers to help with the usage of the API. Something like `appname/appversion`, for example `Cool Radio App/1.2`. This also helps me to know which apps are using this service, so I can keep the list of apps up to date and tell people in which ways they can use this service.

[Content type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) should be specified as appropriate.

If you know an app that is using this service but not listed on [www.radio-browser.info](http://www.radio-browser.info), please drop me a note. Thank you! At the moment this service checks radio stations by connecting to them at least every day and marks them accordingly. (`LastCheckOK=0/1`)

If you can't find what you are looking for here, please create a feature request on [Github](https://github.com/segler-alex/radiobrowser-api-rust) or if you are a programmer, fork it and make a pull request. Thanks for your help! Recent changes can be found in the Changelog.

Please note that all the parameters listed below can be added by using an HTTP POST request with the encoding "x-www-form-urlencoded" instead of GET request, and they can also be sent with encoding "application/json" used by Angular.js, for example. 

# Structs

## Station

> **Results:**
    
    
    {
        "changeuuid":"01234567-89ab-cdef-0123-456789abcdef",
        "stationuuid":"01234567-89ab-cdef-0123-456789abcdef",
        "serveruuid":"01234567-89ab-cdef-0123-456789abcdef",
        "name":"Best Radio",
        "url":"http://www.example.com/test.pls",
        "url_resolved":"http://stream.example.com/mp3_128",
        "homepage":"https://www.example.com",
        "favicon":"https://www.example.com/icon.png",
        "tags":"jazz,pop,rock,indie",
        "country":"Switzerland",
        "countrycode":"US",
        "iso_3166_2": "US-NY",
        "state":"",
        "language":"german,english",
        "languagecodes":"ger,eng",
        "votes":0,
        "lastchangetime":"2019-12-12 18:37:02",
        "lastchangetime_iso8601":"2019-12-12T18:37:02Z",
        "codec":"MP3",
        "bitrate":128,
        "hls":0,
        "lastcheckok":1,
        "lastchecktime":"2020-01-09 18:16:35",
        "lastchecktime_iso8601":"2020-01-09T18:16:35Z",
        "lastcheckoktime":"2020-01-09 18:16:35",
        "lastcheckoktime_iso8601":"2020-01-09T18:16:35Z",
        "lastlocalchecktime":"2020-01-08 23:18:38",
        "lastlocalchecktime_iso8601":"2020-01-08T23:18:38Z",
        "clicktimestamp":"",
        "clicktimestamp_iso8601":null,
        "clickcount":0,
        "clicktrend":0,
        "ssl_error": 0,
        "geo_lat": 1.1,
        "geo_long": -2.2,
        "has_extended_info": false
    }
    
    
    
    <station
        changeuuid="01234567-89ab-cdef-0123-456789abcdef"
        stationuuid="01234567-89ab-cdef-0123-456789abcdef"
        serveruuid="01234567-89ab-cdef-0123-456789abcdef"
        name="Best radio"
        url="http://www.example.com/test.pls"
        url_resolved="http://stream.example.com/mp3_128"
        homepage="https://www.example.com"
        favicon="https://www.example.com/icon.png"
        tags="jazz,pop,rock,indie"
        country="Switzerland"
        countrycode="US"
        iso_3166_2="US-NY"
        state=""
        language="german,english"
        languagecodes="ger,eng"
        votes="0"
        lastchangetime="2019-12-12 18:37:02"
        lastchangetime_iso8601="2019-12-12T18:37:02Z"
        codec="MP3"
        bitrate="128"
        hls="0"
        lastcheckok="1"
        lastchecktime="2020-01-09 18:16:35"
        lastchecktime_iso8601="2020-01-09T18:16:35Z"
        lastcheckoktime="2020-01-09 18:16:35"
        lastcheckoktime_iso8601="2020-01-09T18:16:35Z"
        lastlocalchecktime="2020-01-08 23:18:38"
        lastlocalchecktime_iso8601="2020-01-08T23:18:38Z"
        clicktimestamp=""
        clickcount="0"
        clicktrend="0"
        ssl_error="0"
        geo_lat="1.1"
        geo_long="-2.2"
        has_extended_info="false"/>
    
    
    
    changeuuid,stationuuid,serveruuid,name,url,url_resolved,homepage,favicon,tags,country,countrycode,iso_3166_2,state,language,languagecodes,votes,lastchangetime,lastchangetime_iso8601,codec,bitrate,hls,lastcheckok,lastchecktime,lastchecktime_iso8601,lastcheckoktime,lastcheckoktime_iso8601,lastlocalchecktime,lastlocalchecktime_iso8601,clicktimestamp,clicktimestamp_iso8601,clickcount,clicktrend,ssl_error,geo_lat,geo_long,has_extended_info
    01234567-89ab-cdef-0123-456789abcdef,01234567-89ab-cdef-0123-456789abcdef,01234567-89ab-cdef-0123-456789abcdef,Best radio,http://www.example.com/test.pls,http://stream.example.com/mp3_128,https://www.example.com,https://www.example.com/icon.png,"jazz,pop,rock,indie",Switzerland,US,US-NY,"german,english","ger,eng",0,
    2019-12-12 18:37:02,2019-12-12T18:37:02Z,MP3,128,0,2020-01-09 18:16:35,2020-01-09T18:16:35Z,2020-01-09 18:16:35,2020-01-09T18:16:35Z,2020-01-08 23:18:38,2020-01-08T23:18:38Z,,0,0,0,1.1,-2.2,false
    
    
    
    #EXTM3U
    #RADIOBROWSERUUID:01234567-89ab-cdef-0123-456789abcdef
    #EXTINF:-1,Best Radio
    http://stream.example.com/mp3_128
    
    #RADIOBROWSERUUID:01234567-89ab-cdef-0123-456789abcdef
    #EXTINF:-1,Other Radio
    http://stream.example2.com/mp3_256
    
    
    
    [playlist]
    NumberOfEntries=2
    Title1=Best Radio
    File1=http://stream.example.com/mp3_128
    
    Title2=Other Radio
    File2=http://stream.example2.com/mp3_256
    
    
    
    <?xml version="1.0" encoding="UTF-8" ?>
    <playlist version="1" xmlns="http://xspf.org/ns/0/">
        <trackList>
            <track>
                <title>Best Radio</title>
                <location>http://stream.example.com/mp3_128</location>
                <image>http://example.com/favicon.ico</image>
                <identifier>radiobrowser:01234567-89ab-cdef-0123-456789abcdef</identifier>
            </track>
            <track>
                <title>Other Radio</title>
                <location>https://stream.example2.com/mp3_256</location>
                <image>http://example2.com/favicon.ico</image>
                <identifier>radiobrowser:11234567-89ab-cdef-0123-456789abcdef</identifier>
            </track>
        </trackList>
    </playlist>
    

### Fields:



Name | Possible value/Datatype | Description  
---|---|---  
`changeuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | A globally unique identifier for the change of the station information  
`stationuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | A globally unique identifier for the station  
`name` | string | The name of the station  
`url` | string, URL (HTTP/HTTPS) | The stream URL provided by the user  
`url_resolved` | string, URL (HTTP/HTTPS) | An automatically "resolved" stream URL. Things resolved are playlists (M3U/PLS/ASX...), HTTP redirects (Code 301/302). This link is especially useful if you use this API from a platform that is not able to do a resolve on its own (e.g. JavaScript in browser) or you just don't want to invest the time in decoding playlists yourself.  
`homepage` | string, URL (HTTP/HTTPS) | URL to the homepage of the stream, so you can direct the user to a page with more information about the stream.  
`favicon` | string, URL (HTTP/HTTPS) | URL to an icon or picture that represents the stream. (PNG, JPG)  
`tags` | string, multivalue, split by comma | Tags of the stream with more information about it  
`country` | string | DEPRECATED: use `countrycode` instead, full name of the country. Currently it is autogenerated from the countrycode.  
`countrycode` | 2 letters, uppercase | Official `countrycodes` as in [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)  
`state` | string | Full name of the entity where the station is located inside the country  
`language` | string, multivalue, split by comma | Languages that are spoken in this stream.  
`languagecodes` | string, multivalue, split by comma | Languages that are spoken in this stream by code [ISO 639-2/B](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)  
`votes` | number, integer | Number of votes for this station. This number is by server and only ever increases. It will never be reset to 0.  
`lastchangetime` | datetime, YYYY-MM-DD HH:mm:ss | Last time when the stream information was changed in the database  
`lastchangetime_iso8601` | datetime, [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) | Last time when the stream information was changed in the database  
`codec` | string | The codec of this stream recorded at the last check.  
`bitrate` | number, integer, bps | The bitrate of this stream recorded at the last check.  
`hls` | `0` or `1` | Mark if this stream is using HLS distribution or non-HLS.  
`lastcheckok` | `0` or `1` | The current online/offline state of this stream. This is a value calculated from multiple measure points in the internet. The test servers are located in different countries. It is a majority vote.  
`lastchecktime` | datetime, YYYY-MM-DD HH:mm:ss | The last time when any radio-browser server checked the online state of this stream  
`lastchecktime_iso8601` | datetime, [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) | The last time when any radio-browser server checked the online state of this stream  
`lastcheckoktime` | datetime, YYYY-MM-DD HH:mm:ss | The last time when the stream was checked for the online status with a positive result  
`lastcheckoktime_iso8601` | datetime, [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) | The last time when the stream was checked for the online status with a positive result  
`lastlocalchecktime` | datetime, YYYY-MM-DD HH:mm:ss | The last time when this server checked the online state and the metadata of this stream  
`lastlocalchecktime_iso8601` | datetime, [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) | The last time when this server checked the online state and the metadata of this stream  
`clicktimestamp` | datetime, YYYY-MM-DD HH:mm:ss | The time of the last click recorded for this stream  
`clicktimestamp_iso8601` | datetime, [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) | The time of the last click recorded for this stream  
`clickcount` | number, integer | Clicks within the last 24 hours  
`clicktrend` | number, integer | The difference of the click-counts within the last 2 days. Positive values mean an increase, negative a decrease of clicks.  
`ssl_error` | number, integer | `0` means no error, `1` means that there was an ssl error while connecting to the stream url.  
`geo_lat` | number, double | Latitude on earth where the stream is located.  
`geo_long` | number, double | Longitude on earth where the stream is located.  
`has_extended_info` | bool, optional | Is `true`, if the stream owner does provide extended information as HTTP headers which override the information in the database.

  The **M3U** files created by this server are extended with an additional field, that can be used to identify entries of the file with this server. The field is added as a special comment, so it will not interfere with normal operations of players, that use this playlist.  The **XSPF** files created by this server are extended with an additional field, that can be used to identify entries of the file with this server. We try to be consistent with the specification at <https://xspf.org/orig-xspf-v1.html>

## Station check

This struct is used to represent an online check of a stream. Most of the information gets extracted by checking the [http headers of the stream](https://www.stream-meta.info/).

> **Results:**
    
    
    {
        "stationuuid":"960e57c5-0601-11e8-ae97-52543be04c81",
        "checkuuid":"18be4561-309a-11ea-b37a-0242ac120002",
        "source":"de1.api.radio-browser.info",
        "codec":"MP3",
        "bitrate":128,
        "hls":0,
        "ok":1,
        "timestamp_iso8601":"2020-01-06T15:34:58Z",
        "timestamp":"2020-01-06 15:34:58",
        "urlcache":"http://stream.example.com/mp3_128",
        "metainfo_overrides_database":0,
        "public":null,
        "name":null,
        "description":null,
        "tags":null,
        "countrycode":null,
        "homepage":null,
        "favicon":null,
        "loadbalancer":null,
        "do_not_index":null,
        "countrysubdivisioncode": null,
        "server_software": "Icecast 2.4.0",
        "sampling": 44100,
        "timing_ms": 495,
        "languagecodes": null,
        "ssl_error": 0,
        "geo_lat": 1.1,
        "geo_long": -2.2
    }
    
    
    
    <check
        stationuuid="01234567-89ab-cdef-0123-456789abcdef"
        checkuuid="01234567-89ab-cdef-0123-456789abcdef"
        source="de1.api.radio-browser.info"
        codec="MP3"
        bitrate="128"
        hls="0"
        ok="1"
        urlcache="http://stream.example.com/mp3_128"
        timestamp_iso8601="2020-01-06T15:34:58Z"
        timestamp="2020-01-06 15:34:58"
        urlcache="http://stream.example.com/mp3_128"
        metainfo_overrides_database="0"
        public="0"
        name=""
        description=""
        tags=""
        countrycode=""
        homepage=""
        favicon=""
        loadbalancer=""
        do_not_index=""
        countrysubdivisioncode=""
        server_software="Icecast 2.4.2"
        sampling="44100"
        timing_ms="495"
        languagecodes=""
        ssl_error="0"
        geo_lat="1.1"
        geo_long="-2.2"/>
    
    
    
    stationuuid,checkuuid,source,codec,bitrate,hls,ok,timestamp_iso8601,timestamp,urlcache,metainfo_overrides_database,public,name,description,tags,countrycode,homepage,favicon,loadbalancer,do_not_index,countrysubdivisioncode,server_software,sampling,timing_ms,languagecodes,ssl_error,geo_lat,geo_long
    01234567-89ab-cdef-0123-456789abcdef,01234567-89ab-cdef-0123-456789abcdef,de1.api.radio-browser.info,MP3,192,0,1,2021-04-16T08:07:45Z,2021-04-16 08:07:45,http://stream.example.com/mp3_128,0,,,,,,,,,,,Icecast 2.4.2,,495,,0,,
    

### Fields:



Name | Possible value/Datatype | Description | Nullable  
---|---|---|---  
`checkuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | An unique id for this StationCheck | NO  
`stationuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | An unique id for referencing a Station | NO  
`source` | string | DNS Name of the server that did the stream check. | NO  
`codec` | string | High level name of the used codec of the stream. May have the format AUDIO or AUDIO/VIDEO. | NO  
`bitrate` | number, integer | Bitrate 1000 bits per second (kBit/s) of the stream. (Audio + Video) | NO  
`hls` | number, integer | `1` means this is an [HLS stream](https://en.wikipedia.org/wiki/HTTP_Live_Streaming), otherwise `0`. | NO  
`ok` | number, integer | 1 means this stream is reachable, otherwise 0. | NO  
`timestamp_iso8601` | [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) datetime string | Date and time of check creation | NO  
`timestamp` | datetime, YYYY-MM-DD HH:mm:ss | Date and time of check creation | NO  
`urlcache` | string, URL (HTTP/HTTPS) | Direct stream url that has been resolved from the main stream url. HTTP redirects and playlists have been decoded. If hls is `1` then this is still a HLS-playlist. | NO  
`metainfo_overrides_database` | number, integer | `1` means this stream has provided extended information and it should be used to override the local database, otherwise `0`. | NO  
`public` | number, integer | 1 that this stream appears in the public shoutcast/icecast directory, otherwise 0. | YES  
`name` | string | The name extracted from the stream header. | YES  
`description` | string | The description extracted from the stream header. | YES  
`tags` | string | Komma separated list of tags. (genres of this stream) | YES  
`countrycode` | string | Official country-codes as in [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) | YES  
`countrysubdivisioncode` | string | Official country subdivision codes as in [ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2) | YES  
`homepage` | string | The homepage extracted from the stream header. | YES  
`favicon` | string | The favicon extracted from the stream header. | YES  
`loadbalancer` | string | The loadbalancer extracted from the stream header. | YES  
`server_software` | string | The name of the server software used. | YES  
`sampling` | number, unsigned integer | Audio sampling frequency in Hz | YES  
`timing_ms` | number, unsigned integer | Timespan in miliseconds this check needed to be finished. | NO  
`languagecodes` | string | The description extracted from the stream header. | YES  
`ssl_error` | number, unsigned integer | 1 means that a ssl error occured while connecting to the stream, 0 otherwise. | NO  
`geo_lat` | number, double | Latitude on earth where the stream is located. | YES  
`geo_long` | number, double | Longitude on earth where the stream is located. | YES

 

## Station check step

This struct is used in a tree structure to represent all codepaths that were necessary to check an address of a single stream. Steps can cause multiple other steps for example playlists.

> **Results:**
    
    
    {
        "stepuuid": "01234567-89ab-cdef-0123-456789abcdef",
        "parent_stepuuid": "01234567-89ab-cdef-0123-456789abcdef",
        "checkuuid": "01234567-89ab-cdef-0123-456789abcdef",
        "stationuuid": "01234567-89ab-cdef-0123-456789abcdef",
        "url": "http://stream.example.com:8000/streamname",
        "urltype": "STREAM",
        "error": "BadError",
        "creation_iso8601": "2021-04-13T20:11:19Z"
    }
    
    
    
    <checkstep
        stepuuid="01234567-89ab-cdef-0123-456789abcdef"
        parent_stepuuid="01234567-89ab-cdef-0123-456789abcdef"
        checkuuid="01234567-89ab-cdef-0123-456789abcdef"
        stationuuid="01234567-89ab-cdef-0123-456789abcdef"
        url="http://stream.example.com:8000/streamname"
        urltype="STREAM"
        error="BadError"
        creation_iso8601="2021-04-13T20:11:19Z"/>
    
    
    
    stepuuid,parent_stepuuid,checkuuid,stationuuid,url,urltype,error,creation_iso8601
    01234567-89ab-cdef-0123-456789abcdef,01234567-89ab-cdef-0123-456789abcdef,01234567-89ab-cdef-0123-456789abcdef,01234567-89ab-cdef-0123-456789abcdef,http://stream.example.com:8000/streamname,STREAM,BadError,2021-04-13T20:11:19Z
    

### Fields:



Name | Possible value/Datatype | Description | Nullable  
---|---|---|---  
`stepuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | An unique id for this StationCheckStep | NO  
`parent_stepuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | An unique id for referencing another StationCheckStep. Is set if this step has a parent. | YES  
`checkuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | An unique id for referencing a StationCheck | NO  
`stationuuid` | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | An unique id for referencing a Station | NO  
`url` | string, URL (HTTP/HTTPS) | The url that this step of the checking process handled | NO  
`urltype` | string | Does represent which kind of url it is. One of the following: STREAM, REDIRECT, PLAYLIST. | YES  
`error` | string | URL to the homepage of the stream, so you can direct the user to a page with more information about the stream. | YES  
`creation_iso8601` | [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) datetime string | Date and time of step creation | NO

 

# Lists

## List of radio stations

> **Syntax:**
    
    
    /json/stations/byuuid/{searchterm}
    /json/stations/byname/{searchterm}
    /json/stations/bynameexact/{searchterm}
    /json/stations/bycodec/{searchterm}
    /json/stations/bycodecexact/{searchterm}
    /json/stations/bycountry/{searchterm}
    /json/stations/bycountryexact/{searchterm}
    /json/stations/bycountrycodeexact/{searchterm}
    /json/stations/bystate/{searchterm}
    /json/stations/bystateexact/{searchterm}
    /json/stations/bylanguage/{searchterm}
    /json/stations/bylanguageexact/{searchterm}
    /json/stations/bytag/{searchterm}
    /json/stations/bytagexact/{searchterm}
    
    
    
    /xml/stations/byuuid/{searchterm}
    /xml/stations/byname/{searchterm}
    /xml/stations/bynameexact/{searchterm}
    /xml/stations/bycodec/{searchterm}
    /xml/stations/bycodecexact/{searchterm}
    /xml/stations/bycountry/{searchterm}
    /xml/stations/bycountryexact/{searchterm}
    /xml/stations/bycountrycodeexact/{searchterm}
    /xml/stations/bystate/{searchterm}
    /xml/stations/bystateexact/{searchterm}
    /xml/stations/bylanguage/{searchterm}
    /xml/stations/bylanguageexact/{searchterm}
    /xml/stations/bytag/{searchterm}
    /xml/stations/bytagexact/{searchterm}
    
    
    
    /csv/stations/byuuid/{searchterm}
    /csv/stations/byname/{searchterm}
    /csv/stations/bynameexact/{searchterm}
    /csv/stations/bycodec/{searchterm}
    /csv/stations/bycodecexact/{searchterm}
    /csv/stations/bycountry/{searchterm}
    /csv/stations/bycountryexact/{searchterm}
    /csv/stations/bycountrycodeexact/{searchterm}
    /csv/stations/bystate/{searchterm}
    /csv/stations/bystateexact/{searchterm}
    /csv/stations/bylanguage/{searchterm}
    /csv/stations/bylanguageexact/{searchterm}
    /csv/stations/bytag/{searchterm}
    /csv/stations/bytagexact/{searchterm}
    
    
    
    /m3u/stations/byuuid/{searchterm}
    /m3u/stations/byname/{searchterm}
    /m3u/stations/bynameexact/{searchterm}
    /m3u/stations/bycodec/{searchterm}
    /m3u/stations/bycodecexact/{searchterm}
    /m3u/stations/bycountry/{searchterm}
    /m3u/stations/bycountryexact/{searchterm}
    /m3u/stations/bycountrycodeexact/{searchterm}
    /m3u/stations/bystate/{searchterm}
    /m3u/stations/bystateexact/{searchterm}
    /m3u/stations/bylanguage/{searchterm}
    /m3u/stations/bylanguageexact/{searchterm}
    /m3u/stations/bytag/{searchterm}
    /m3u/stations/bytagexact/{searchterm}
    
    
    
    /pls/stations/byuuid/{searchterm}
    /pls/stations/byname/{searchterm}
    /pls/stations/bynameexact/{searchterm}
    /pls/stations/bycodec/{searchterm}
    /pls/stations/bycodecexact/{searchterm}
    /pls/stations/bycountry/{searchterm}
    /pls/stations/bycountryexact/{searchterm}
    /pls/stations/bycountrycodeexact/{searchterm}
    /pls/stations/bystate/{searchterm}
    /pls/stations/bystateexact/{searchterm}
    /pls/stations/bylanguage/{searchterm}
    /pls/stations/bylanguageexact/{searchterm}
    /pls/stations/bytag/{searchterm}
    /pls/stations/bytagexact/{searchterm}
    

> **Results:**
> 
> Details at struct '[Station](https://docs.radio-browser.info/#station)'
    
    
    [
        {
            "name": "..",
            ...
        },
        {
            ...
        },
        {
            ...
        },
        ...
    ]
    
    
    
    <result>
        <station name=".." ... >
        <station name=".." ... >
        <station name=".." ... >
        ...
    </result>
    
    
    
    changeuuid,stationuuid,serveruuid,name,url,url_resolved,homepage,favicon,tags,country,countrycode,iso_3166_2,state,language,languagecodes,votes,lastchangetime,lastchangetime_iso8601,codec,bitrate,hls,lastcheckok,lastchecktime,lastchecktime_iso8601,lastcheckoktime,lastcheckoktime_iso8601,lastlocalchecktime,lastlocalchecktime_iso8601,clicktimestamp,clicktimestamp_iso8601,clickcount,clicktrend,ssl_error,geo_lat,geo_long,has_extended_info
    ...
    ...
    
    
    
    #EXTM3U
    #RADIOBROWSERUUID:...
    #EXTINF:...
    ...
    
    ...
    
    
    
    [playlist]
    NumberOfEntries=...
    Title1=...
    File1=...
    
    ...
    

> **Example:**
    
    
    /json/stations/byname/jazz
    /json/stations/bycountry/austria
    /json/stations/bycountryexact/austria
    /json/stations/bycountrycodeexact/at
    /json/stations/bytagexact/320kbps
    /json/stations/bytagexact/320kbps
    
    
    
    /xml/stations/byname/jazz
    /xml/stations/bycountry/austria
    /xml/stations/bycountryexact/austria
    /xml/stations/bycountrycodeexact/at
    /xml/stations/bytagexact/320kbps
    /xml/stations/bytagexact/320kbps
    
    
    
    /csv/stations/byname/jazz
    /csv/stations/bycountry/austria
    /csv/stations/bycountryexact/austria
    /csv/stations/bycountrycodeexact/at
    /csv/stations/bytagexact/320kbps
    /csv/stations/bytagexact/320kbps
    
    
    
    /m3u/stations/byname/jazz
    /m3u/stations/bycountry/austria
    /m3u/stations/bycountryexact/austria
    /m3u/stations/bycountrycodeexact/at
    /m3u/stations/bytagexact/320kbps
    /m3u/stations/bytagexact/320kbps
    
    
    
    /pls/stations/byname/jazz
    /pls/stations/bycountry/austria
    /pls/stations/bycountryexact/austria
    /pls/stations/bycountrycodeexact/at
    /pls/stations/bytagexact/320kbps
    /pls/stations/bytagexact/320kbps
    

A list of radio stations that match the search. The variants with "exact" will only search for perfect matches, and others will search for the station whose attribute contains the search term.

Please use '[station click counter](https://docs.radio-browser.info/#station-click-counter)' API call to let the click be counted, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `url`, `homepage`, `favicon`, `tags`, `country`, `state`, `language`, `votes`, `codec`, `bitrate`, `lastcheckok`, `lastchecktime`, `clicktimestamp`, `clickcount`, `clicktrend`, `changetimestamp`, `random` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset  
`hidebroken` | `false` | `true`, `false` | do list/not list broken stations

 

## List of all radio stations

> **Syntax:**
    
    
    /json/stations
    
    
    
    /xml/stations
    
    
    
    /csv/stations
    
    
    
    /m3u/stations
    
    
    
    /pls/stations
    

> **Results:**
> 
> An array of struct '[Station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations
    
    
    
    /xml/stations
    
    
    
    /csv/stations
    
    
    
    /m3u/stations
    
    
    
    /pls/stations
    

A list of all radio stations. Please use the '[station click counter](https://docs.radio-browser.info/#station-click-counter)' API call to let the click be counted, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `url`, `homepage`, `favicon`, `tags`, `country`, `state`, `language`, `votes`, `codec`, `bitrate`, `lastcheckok`, `lastchecktime`, `clicktimestamp`, `clickcount`, `clicktrend`, `changetimestamp`, `random` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset  
`hidebroken` | `false` | `true`, `false` | do list/not list broken stations

 

## List of codecs

> **Syntax:**
    
    
    /json/codecs
    /json/codecs/<filter>
    
    
    
    /xml/codecs
    /xml/codecs/<filter>
    
    
    
    /csv/codecs
    /csv/codecs/<filter>
    

> **Results:**
    
    
    [
        {
            "name": "AAC",
            "stationcount": "34"
        },
        {
            "name": "AAC+",
            "stationcount": "367"
        },
        ...
    ]
    
    
    
    <result>
        <codec name="AAC" stationcount="34"/>
        <codec name="AAC+" stationcount="367"/>
        ...
    </result>
    
    
    
    name,stationcount
    AAC,2202
    AAC+,5487
    "AAC+,H.264",6
    ...
    

> **Example:**
    
    
    /json/codecs
    /json/codecs/aac
    
    
    
    /xml/codecs
    /xml/codecs/aac
    
    
    
    /csv/codecs
    /csv/codecs/aac
    

A JSON-encoded list of all codecs in the database. If a filter is given, it will only return the ones containing the filter as substring, supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `stationcount` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`hidebroken` | `false` | `true`, `false` | do not count broken stations  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,.... | number of returned datarows (stations) starting with offset

 

## List of countries

> **Syntax**
    
    
    /json/countries
    /json/countries/<filter>
    
    
    
    /xml/countries
    /xml/countries/<filter>
    
    
    
    /csv/countries
    /csv/countries/<filter>
    

> **Result**
    
    
    [
        {
          "name": "Albania",
          "stationcount": "1"
        },
        {
          "name": "Argentina",
          "stationcount": "5"
        },
        ...
    ]
    
    
    
    <result>
        <country name="Albania" stationcount="1"/>
        <country name="Argentina" stationcount="5"/>
        ...
    </result>
    
    
    
    name,stationcount
    Albania,1
    Argentina,5
    ...
    

> **Example:**
    
    
    /json/countries
    /json/countries/aus
    
    
    
    /xml/countries
    /xml/countries/aus
    
    
    
    /csv/countries
    /csv/countries/aus
    

A JSON-encoded list of all countries in the database. If a filter is given, it will only return the ones containing the filter as substring, supported output formats: JSON, XML, CSV.

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `stationcount` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`hidebroken` | `false` | `true`, `false` | do not count broken stations  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset

 

## List of country codes

> **Syntax:**
    
    
    /json/countrycodes
    /json/countrycodes/<filter>
    
    
    
    /xml/countrycodes
    /xml/countrycodes/<filter>
    
    
    
    /csv/countrycodes
    /csv/countrycodes/<filter>
    

> **Result:**
    
    
    [
        {
          "name": "AT",
          "stationcount": "1"
        },
        {
          "name": "DE",
          "stationcount": "5"
        },
        ...
    ]
    
    
    
    <result>
        <country name="AT" stationcount="1"/>
        <country name="DE" stationcount="5"/>
        ...
    </result>
    
    
    
    name,stationcount
    AT,1
    DE,5
    ...
    

> **Example:**
    
    
    /json/countrycodes
    /json/countrycodes/at
    
    
    
    /xml/countrycodes/
    /xml/countrycodes/at
    
    
    
    /csv/countrycodes/
    /csv/countrycodes/at
    

A JSON-encoded list of all countries in the database. If a filter is given, it will only return the ones containing the filter as substring, supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `stationcount` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`hidebroken` | `false` | `true`, `false` | do not count broken stations  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned data rows (stations) starting with offset

 

## List of states

> **Syntax:**
    
    
    /json/states
    /json/states/<filter>
    /json/states/<country>/<filter>
    
    
    
    /xml/states
    /xml/states/<filter>
    /xml/states/<country>/<filter>
    
    
    
    /csv/states
    /csv/states/<filter>
    /csv/states/<country>/<filter>
    

> **Results:**
    
    
    [
        {
            "name": "Alabama",
            "country": "United States of America",
            "stationcount": "6"
        },
        {
            "name": "Alberta",
            "country": "Canada",
            "stationcount": "2"
        },
        ...
    ]
    
    
    
    <result>
        <state name="Alabama" country="United States of America" stationcount="6"/>
        <state name="Alberta" country="Canada" stationcount="2"/>
        ...
    </result>
    
    
    
    name,country,stationcount
    Alabama,United States of America,6
    Alberta,Canada,2
    

> **Example:**
    
    
    /json/states
    /json/states/ber
    /json/states/Germany/ber
    
    
    
    /xml/states
    /xml/states/ber
    /xml/states/Germany/ber
    
    
    
    /csv/states
    /csv/states/ber
    /csv/states/Germany/ber
    

A JSON-encoded list of all states in the database. Countries are divided into states. If a filter is given, it will only return the ones containing the filter as substring. If a country is given, it will only display states in this country, supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `stationcount` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`hidebroken` | `false` | `true`, `false` | do not count broken stations  
`country` |  | string | OPTIONAL, filter states by country name  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,.... | number of returned datarows (stations) starting with offset

 

## List of languages

> **Syntax:**
    
    
    /json/languages
    /json/languages/<filter>
    
    
    
    /xml/languages
    /xml/languages/<filter>
    
    
    
    /csv/languages
    /csv/languages/<filter>
    

> **Results:**
    
    
    [
        {
            "name": "albanian",
            "iso_639": "sq",
            "stationcount": "1"
        },
        {
            "name": "american english",
            "iso_639": null,
            "stationcount": "8"
        },
        ...
    ]
    
    
    
    <result>
        <language name="albanian" iso_639="sq" stationcount="1"/>
        <language name="american english" stationcount="8"/>
        ...
    </result>
    
    
    
    name,iso_639,stationcount
    albanian,sq,1
    american english,,8
    ...
    

> **Example:**
    
    
    /json/languages
    /json/languages/ger
    
    
    
    /xml/languages
    /xml/languages/ger
    
    
    
    /csv/languages
    /csv/languages/ger
    

A JSON-encoded list of all languages in the database. If a filter is given, it will only return the ones containing the filter as substring, supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `stationcount` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`hidebroken` | `false` | `true`, `false` | do not count broken stations  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset

 

## List of tags

> **Syntax:**
    
    
    /json/tags
    /json/tags/<filter>
    
    
    
    /xml/tags
    /xml/tags/<filter>
    
    
    
    /csv/tags
    /csv/tags/<filter>
    

> **Results:**
    
    
    [
        {
            "name": "00s",
            "stationcount": "3"
        },
        {
            "name": "10s",
            "stationcount": "1"
        },
        ..
    ]
    
    
    
    <result>
        <tag name="00s" stationcount="3"/>
        <tag name="10s" stationcount="1"/>
        ...
    </result>
    
    
    
    name,stationcount
    00s,3
    10s,1
    

> **Example:**
    
    
    /json/tags
    /json/tags/jazz
    
    
    
    /xml/tags
    /xml/tags/jazz
    
    
    
    /csv/tags
    /csv/tags/jazz
    

A JSON-encoded list of all tags in the database. If a filter is given, it will only return the ones containing the filter as substring, supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`order` | `name` | `name`, `stationcount` | name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | reverse the result list if set to `true`  
`hidebroken` | `false` | `true`, `false` | do not count broken stations  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | 100000 | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset

 

## List of station clicks

> **Syntax:**
    
    
    /json/clicks
    /json/clicks/stationuuid
    
    
    
    /xml/clicks
    /xml/clicks/stationuuid
    
    
    
    /csv/clicks
    /csv/clicks/stationuuid
    

> **Results:**
    
    
    [
        {
            "stationuuid":"963134e8-0601-11e8-ae97-52543be04c81",
            "clickuuid":"ce9ad7bd-34bf-11ea-ac52-52543be04c81",
            "clicktimestamp_iso8601":"2020-01-11T23:14:58Z",
            "clicktimestamp":"2020-01-11 23:14:58"
        },
        {
            "stationuuid":"2a70c205-4850-11e8-b1b0-52543be04c81",
            "clickuuid":"cf49f517-34bf-11ea-ac52-52543be04c81",
            "clicktimestamp_iso8601":"2020-01-11T23:15:00Z"
            "clicktimestamp":"2020-01-11 23:15:00"
        },
        ...
    ]
    
    
    
    <click
        stationuuid="961fa288-0601-11e8-ae97-52543be04c81"
        clickuuid="87a69149-34c1-11ea-ac52-52543be04c81"
        clicktimestamp_iso8601="2020-01-11T23:27:18Z"
        clicktimestamp="2020-01-11 23:27:18"
    />
    <click
        stationuuid="7a25bf68-1dbe-11ea-a955-52543be04c81"
        clickuuid="a25e5fb6-34c1-11ea-ac52-52543be04c81"
        clicktimestamp_iso8601="2020-01-11T23:28:03Z"
        clicktimestamp="2020-01-11 23:28:03"
    />
    
    
    
    stationuuid,clickuuid,clicktimestamp_iso8601,clicktimestamp
    961fa288-0601-11e8-ae97-52543be04c81,87a69149-34c1-11ea-ac52-52543be04c81,2020-01-11T23:27:18Z,2020-01-11 23:27:18
    7a25bf68-1dbe-11ea-a955-52543be04c81,a25e5fb6-34c1-11ea-ac52-52543be04c81,2020-01-11T23:28:03Z,2020-01-11 23:28:03
    

> **Example:**
    
    
    /json/clicks
    /json/clicks?seconds=3600
    
    
    
    /xml/clicks
    /xml/clicks?seconds=3600
    
    
    
    /csv/clicks
    /csv/clicks?seconds=3600
    

A list of station clicks. If a station UUID is provided, only clicks of the station will be returned. If a station UUID is not provided, a list of all clicks of all stations will be sent (chunksize 10000), supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`stationuuid` |  | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | If set, only list check result of the matching station.  
`lastclickuuid` |  | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | If set, only list clicks after the click with the given uuid. Use this to continue chunked retrieval to get the next 10000 clicks.  
`seconds` | `0` | positive integer values | if >`0`, it will only return history entries from the last 'seconds' seconds.

 

## List of station check results

> **Syntax:**
    
    
    /json/checks
    /json/checks/stationuuid
    
    
    
    /xml/checks
    /xml/checks/stationuuid
    
    
    
    /csv/checks
    /csv/checks/stationuuid
    

> **Results:**
> 
> Details at struct '[Station check](https://docs.radio-browser.info/#station-check)'
> 
> **Example:**
    
    
    /json/checks
    
    
    
    /xml/checks
    
    
    
    /csv/checks
    

A list of station check results. If a station UUID is provided, the whole history will be returned. If a station ID is not provided, a list of all last checks of all stations will be sent (without older check results), supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`stationuuid` |  | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | If set, only list check result of the matching station.  
`lastcheckuuid` |  | [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) | If set, only list checks after the check with the given check.  
`seconds` | `0` | positive integer values | if >`0`, it will only return history entries from the last 'seconds' seconds.  
`limit` | `999999` | `0`,`1`,`2`,`3`... | number of returned datarows (checks)

 

## List of station check steps

> **Syntax:**
    
    
    /json/checksteps
    
    
    
    /xml/checksteps
    
    
    
    /csv/checksteps
    

> **Results:**

Details at struct '[Check step](https://docs.radio-browser.info/#station-check-step)'
    
    
    <result>
        <checkstep stepuuid=".." ... >
        <checkstep stepuuid=".." ... >
        ...
    </result>
    
    
    
    stepuuid
    ...
    ...
    
    

> **Example:**
    
    
    /json/checksteps
    /json/checksteps?uuids=01234567-89ab-cdef-0123-456789abcdef
    
    
    
    /xml/checksteps
    /xml/checksteps?uuids=01234567-89ab-cdef-0123-456789abcdef
    
    
    
    /csv/checksteps
    /csv/checksteps?uuids=01234567-89ab-cdef-0123-456789abcdef
    

A list of steps that needed to be done to finish a station check.

Supported output formats: JSON, XML, CSV

### Parameters:



Name | Example | Description  
---|---|---  
uuids | `01234567-89ab-cdef-0123-456789abcdef,01234567-89ab-cdef-0123-456789abcdef` | MANDATORY, comma-separated list of UUIDs of stations, may be array in JSON

 

## Advanced station search

> **Syntax:**
    
    
    /json/stations/search
    
    
    
    /xml/stations/search
    
    
    
    /csv/stations/search
    
    
    
    /m3u/stations/search
    
    
    
    /pls/stations/search
    

> **Results:**
> 
> Array of struct [Station](https://docs.radio-browser.info/#station)
> 
> **Example:**
    
    
    /json/stations/search
    
    
    
    /xml/stations/search
    
    
    
    /csv/stations/search
    
    
    
    /m3u/stations/search
    
    
    
    /pls/stations/search
    

A list of radio stations that match the search. It will search for the station whose attribute contains the search term. Please use '[Count station click](https://docs.radio-browser.info/#station-click-count)' API call to let the click be counted, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`name` |  | string | OPTIONAL, name of the station  
`nameExact` | `false` | `true`, `false` | OPTIONAL. True: only exact matches, otherwise all matches.  
`country` |  | string | OPTIONAL, country of the station  
`countryExact` | `false` | `true`, `false` | OPTIONAL. True: only exact matches, otherwise all matches.  
`countrycode` |  | string | OPTIONAL, 2-digit countrycode of the station (see [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)).  
`state` |  | string | OPTIONAL, state of the station  
`stateExact` | `false` | `true`, `false` | OPTIONAL. True: only exact matches, otherwise all matches.  
`language` |  | string | OPTIONAL, language of the station  
`languageExact` | `false` | `true`, `false` | OPTIONAL. True: only exact matches, otherwise all matches.  
`tag` |  | string | OPTIONAL, a tag of the station  
`tagExact` | `false` | `true`, `false` | OPTIONAL. True: only exact matches, otherwise all matches.  
`tagList` |  | string, string, ... | OPTIONAL. , a comma-separated list of tag. It can also be an array of string in JSON HTTP POST parameters. All tags in list have to match.  
`codec` |  | string | OPTIONAL, codec of the station  
`bitrateMin` | `0` | POSITIVE INTEGER | OPTIONAL, minimum of kbps for bitrate field of stations in result  
`bitrateMax` | `1000000` | POSITIVE INTEGER | OPTIONAL, maximum of kbps for bitrate field of stations in result  
`has_geo_info` | both | not set, `true`, `false` | OPTIONAL, not set=display all, `true`=show only stations with geo_info, `false`=show only stations without geo_info  
`has_extended_info` | both | not set, `true`, `false` | OPTIONAL, not set=display all, `true`=show only stations which do provide extended information, `false`=show only stations without extended information  
`is_https` | both | not set, `true`, `false` | OPTIONAL, not set=display all, `true`=show only stations which have https url, `false`=show only stations that do stream unencrypted with http  
`order` | `name` | `name`, `url`, `homepage`, `favicon`, `tags`, `country`, `state`, `language`, `votes`, `codec`, `bitrate`, `lastcheckok`, `lastchecktime`, `clicktimestamp`, `clickcount`, `clicktrend`, `changetimestamp`, `random` | OPTIONAL, name of the attribute the result list will be sorted by  
`reverse` | `false` | `true`, `false` | OPTIONAL, reverse the result list if set to `true`  
`offset` | `0` | POSITIVE INTEGER | OPTIONAL, starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | OPTIONAL, number of returned datarows (stations) starting with offset  
`hidebroken` | `false` | `true`, `false` | do list/not list broken stations

 

## Search radio stations by URL

> **Syntax:**
    
    
    /json/stations/byurl
    
    
    
    /xml/stations/byurl
    
    
    
    /csv/stations/byurl
    
    
    
    /m3u/stations/byurl
    
    
    
    /pls/stations/byurl
    

> **Results:**
> 
> Array of struct '[station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations/byurl
    
    
    
    /xml/stations/byurl
    
    
    
    /csv/stations/byurl
    
    
    
    /m3u/stations/byurl
    
    
    
    /pls/stations/byurl
    

A list of radio stations that have an exact URL match, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Example value | Description  
---|---|---  
`url` | `http://this.is.a.link/test.mp3` | MANDATORY, URL of the station

 

## Search radio stations by UUIDs

> **Syntax:**
    
    
    /json/stations/byuuid
    
    
    
    /xml/stations/byuuid
    
    
    
    /csv/stations/byuuid
    
    
    
    /m3u/stations/byuuid
    
    
    
    /pls/stations/byuuid
    

> **Results:**
> 
> Array of struct '[station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations/byuuid
    
    
    
    /xml/stations/byuuid
    
    
    
    /csv/stations/byuuid
    
    
    
    /m3u/stations/byuuid
    
    
    
    /pls/stations/byuuid
    

A list of radio stations that have an exact UUID match, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Example value | Description  
---|---|---  
`uuids` | `110e57c5-0601-11e8-ae97-52543be04c81,220e57c5-0601-11e8-ae97-52543be04c81,330e57c5-0601-11e8-ae97-52543be04c81` | MANDATORY, comma-separated list of UUIDs

 

## Server config

> **Syntax:**
    
    
    /json/config
    
    
    
    /xml/config
    

> **Results:**
    
    
    {
        "check_enabled": false,
        "prometheus_exporter_enabled": true,
        "pull_servers": [
            "http://www.radio-browser.info/webservice",
            "http://de1.api.radio-browser.info"
        ],
        "tcp_timeout_seconds": 10,
        "broken_stations_never_working_timeout_seconds": 259200,
        "broken_stations_timeout_seconds": 2592000,
        "checks_timeout_seconds": 2592000,
        "click_valid_timeout_seconds": 86400,
        "clicks_timeout_seconds": 2592000,
        "mirror_pull_interval_seconds": 300,
        "update_caches_interval_seconds": 300,
        "server_name": "gaia",
        "server_location": "Datacenter 2 in coolstreet",
        "server_country_code": "DE",
        "check_retries": 5,
        "check_batchsize": 100,
        "check_pause_seconds": 60,
        "api_threads": 5,
        "cache_type": "redis",
        "cache_ttl": 60
    }
    
    
    
    <config>
        <check_enabled>false</check_enabled>
        <prometheus_exporter_enabled>true</prometheus_exporter_enabled>
        <pull_servers>
            <url>http://www.radio-browser.info/webservice</url>
            <url>http://de1.api.radio-browser.info</url>
        </pull_servers>
        <tcp_timeout_seconds>10</tcp_timeout_seconds>
        <broken_stations_never_working_timeout_seconds>259200</broken_stations_never_working_timeout_seconds>
        <broken_stations_timeout_seconds>2592000</broken_stations_timeout_seconds>
        <checks_timeout_seconds>2592000</checks_timeout_seconds>
        <click_valid_timeout_seconds>86400</click_valid_timeout_seconds>
        <clicks_timeout_seconds>2592000</clicks_timeout_seconds>
        <mirror_pull_interval_seconds>300</mirror_pull_interval_seconds>
        <update_caches_interval_seconds>300</update_caches_interval_seconds>
        <server_name>gaia</server_name>
        <server_location>Datacenter 2 in coolstreet</server_location>
        <server_country_code>DE</server_country_code>
        <check_retries>5</check_retries>
        <check_batchsize>100</check_batchsize>
        <check_pause_seconds>60</check_pause_seconds>
        <api_threads>5</api_threads>
        <cache_type>redis</cache_type>
        <cache_ttl>60</cache_ttl>
    </config>
    

> **Example:**
    
    
    /json/config
    
    
    
    /xml/config
    

The current active server config, supported output formats: JSON, XML

## Server mirrors

> **Syntax:**
    
    
    /json/servers
    

> **Results:**
    
    
    [
        {
            "ip": "95.179.139.106",
            "name": "nl1.api.radio-browser.info"
        },
        {
            "ip": "188.68.62.16",
            "name": "de1.api.radio-browser.info"
        },
        {
            "ip": "2a03:4000:6:8077::1",
            "name": "de1.api.radio-browser.info"
        },
        {
            "ip": "2001:19f0:5001:32a4:5400:2ff:fe37:75c2",
            "name": "nl1.api.radio-browser.info"
        }
    ]
    

> **Example:**
    
    
    /json/servers
    

A list of server mirrors. A DNS look-up of all.api.radio-browser.info is performed followed by a reverse one for every result getting from the first request. This should be done on the client. ONLY USE THIS if your client is not able to do DNS look-ups, supported output formats: JSON

## Prometheus monitoring

> **Syntax:**
    
    
    /metrics
    

> **Results:**
    
    
    # HELP radio_browser_clicks_last_hour Clicks in the last hour
    # TYPE radio_browser_clicks_last_hour gauge
    radio_browser_clicks_last_hour 0
    
    # HELP radio_browser_stations_broken Count of stations that are broken
    # TYPE radio_browser_stations_broken gauge
    radio_browser_stations_broken 740
    
    # HELP radio_browser_stations_working Count of stations that are working/usable
    # TYPE radio_browser_stations_working gauge
    radio_browser_stations_working 26514
    
    # HELP radio_browser_stations_todo Count of stations that need are in the queue for checking
    # TYPE radio_browser_stations_todo gauge
    radio_browser_stations_todo 27254
    
    # HELP radio_browser_stations_deletable_never_worked Count of stations that are in the list for deletion and which never worked
    # TYPE radio_browser_stations_deletable_never_worked gauge
    radio_browser_stations_deletable_never_worked 0
    
    # HELP radio_browser_stations_deletable_were_working Count of stations that are in the list for deletion and which worked at some point
    # TYPE radio_browser_stations_deletable_were_working gauge
    radio_browser_stations_deletable_were_working 0
    

> **Example:**
    
    
    /metrics
    

Exporter for [prometheus](https://prometheus.io/). It renders internal data about the server in a specific format that is readable by the time series database prometheus.

## Server stats

> **Syntax:**
    
    
    /json/stats
    
    
    
    /xml/stats
    

> **Results:**
    
    
    {
        "supported_version": 1,
        "software_version": "0.5.0",
        "status": "OK",
        "stations": 4047,
        "stations_broken": 45,
        "tags": 677,
        "clicks_last_hour": 65,
        "clicks_last_day": 1822,
        "languages": 59,
        "countries": 81
    }
    
    
    
    <result>
        <stats
            supported_version="1"
            software_version="0.5.0"
            status="OK"
            stations="4047"
            stations_broken="45"
            tags="677"
            clicks_last_hour="66"
            clicks_last_day="1824"
            languages="59"
            countries="81"
        />
    </result>
    

> **Example:**
    
    
    /json/stats
    
    
    
    /xml/stats
    

Web service stats, supported output formats: JSON, XML

# Modify

## Add radio station

> **Syntax:**
    
    
    /json/add
    
    
    
    /xml/add
    

> **Results:**
    
    
    {
        "ok": true,
        "message": "station was added",
        "uuid": "550e8400-e29b-11d4-a716-446655440000"
    }
    
    
    
    <result>
        <status ok="true"
        message="station was added"
        uuid="550e8400-e29b-11d4-a716-446655440000"
    </result>
    

> **Example:**
    
    
    /json/add
    
    
    
    /xml/add
    

Add a radio station to the database, supported output formats: JSON, XML

### Parameters:



Name | Example value | Description  
---|---|---  
`name` | `Station Name` | MANDATORY, the name of the radio station. Max 400 chars.  
`url` | `http://this.is.an.url/stream.mp3` | MANDATORY, the URL of the station  
`homepage` | `http://this.is.an.url/` | the homepage URL of the station  
`favicon` | `http://this.is.an.url/favicon.ico` | the URL of an image file (jpg or png)  
`countrycode` | `AT` | The 2 letter countrycode of the country where the radio station is located  
`state` | `Vienna` | The name of the part of the country where the station is located  
`language` | `English` | The main language used in spoken text parts of the radio station  
`tags` | `pop,rock` | A list of tags separated by commas to describe the station  
`geo_lat` | `12.3456` | The latitude of the stream location. Nullable.  
`geo_long` | `-12.3456` | The longitude of the stream location. Nullable.

 

## Station click counter

> **Syntax:**
    
    
    /json/url/stationuuid
    
    
    
    /xml/url/stationuuid
    
    
    
    /m3u/url/stationuuid
    
    
    
    /pls/url/stationuuid
    

> **Results:**
    
    
    {
        "ok": "true",
        "message": "retrieved station url",
        "stationuuid": "9617a958-0601-11e8-ae97-52543be04c81",
        "name": "Station name",
        "url": "http://this.is.an.url"
    }
    
    
    
    <result>
        <status 
            ok="true" 
            message="retrieved station url" 
            stationuuid="9617a958-0601-11e8-ae97-52543be04c81" 
            name="Station name" 
            url="http://this.is.an.url"
        />
    </result>
    
    
    
    #EXTM3U
    #RADIOBROWSERUUID:9617a958-0601-11e8-ae97-52543be04c81
    #EXTINF:1,Station name
    http://this.is.an.url
    
    
    
    [playlist]
    NumberOfEntries=1
    Title1=Station name
    File1=http://this.is.an.url
    

> **Example:**
    
    
    /json/url/123
    
    
    
    /xml/url/123
    
    
    
    /m3u/url/123
    
    
    
    /pls/url/123
    

Increase the click count of a station by one. This should be called everytime when a user starts playing a stream to mark the stream more popular than others. Every call to this endpoint from the same IP address and for the same station only gets counted once per day. The call will return detailed information about the stream, supported output formats: JSON, XML, PLS, M3U

## Vote for a station

> **Syntax:**
    
    
    /json/vote/stationuuid
    
    
    
    /xml/vote/stationuuid
    

> **Results:**
    
    
    {
        "ok": true,
        "message": "voted for station successfully"
    }
    
    
    
    <result>
        <status ok="true" message="voted for station successfully"/>
    </result>
    

> **Example:**
    
    
    /json/vote/123
    
    
    
    /xml/vote/123
    

Increase the vote count for the station by one. Can only be done by the same IP address for one station every 10 minutes. If it works, the changed station will be returned as result, supported output formats: JSON, XML

# Stations

## Broken stations
    
    
    /json/stations/broken
    /json/stations/broken/rowcount
    
    
    
    /xml/stations/broken
    /xml/stations/broken/rowcount
    
    
    
    /csv/stations/broken
    /csv/stations/broken/rowcount
    
    
    
    /m3u/stations/broken
    /m3u/stations/broken/rowcount
    
    
    
    /pls/stations/broken
    /pls/stations/broken/rowcount
    

> **Results:**
> 
> Array of struct '[station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations/broken?limit=5
    /json/stations/broken/5
    
    
    
    /xml/stations/broken?limit=5
    /xml/stations/broken/5
    
    
    
    /csv/stations/broken?limit=5
    /csv/stations/broken/5
    
    
    
    /m3u/stations/broken?limit=5
    /m3u/stations/broken/5
    
    
    
    /pls/stations/broken?limit=5
    /pls/stations/broken/5
    

A list of the stations that did not pass the connection test, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset

 

## Stations by clicks

> **Syntax:**
    
    
    /xml/stations/topclick
    /xml/stations/topclick/rowcount
    
    
    
    /json/stations/topclick
    /json/stations/topclick/rowcount
    
    
    
    /csv/stations/topclick
    /csv/stations/topclick/rowcount
    
    
    
    /m3u/stations/topclick
    /m3u/stations/topclick/rowcount
    
    
    
    /pls/stations/topclick
    /pls/stations/topclick/rowcount
    

> **Results:**
> 
> Array of struct '[station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations/topclick
    /json/stations/topclick/5
    
    
    
    /xml/stations/topclick
    /xml/stations/topclick/5
    
    
    
    /csv/stations/topclick
    /csv/stations/topclick/5
    
    
    
    /m3u/stations/topclick
    /m3u/stations/topclick/5
    
    
    
    /pls/stations/topclick
    /pls/stations/topclick/5
    

A list of the stations that are clicked the most. You can add a parameter with the number of wanted stations, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset  
`hidebroken` | `false` | `true`, `false` | do list/not list broken stations

 

## Stations by recent clicks

> **Syntax:**
    
    
    /json/stations/lastclick
    /json/stations/lastclick/rowcount
    
    
    
    /xml/stations/lastclick
    /xml/stations/lastclick/rowcount
    
    
    
    /csv/stations/lastclick
    /csv/stations/lastclick/rowcount
    
    
    
    /m3u/stations/lastclick
    /m3u/stations/lastclick/rowcount
    
    
    
    /pls/stations/lastclick
    /pls/stations/lastclick/rowcount
    

> **Results:**
> 
> Array of struct '[station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations/lastclick
    /json/stations/lastclick/5
    
    
    
    /xml/stations/lastclick
    /xml/stations/lastclick/5
    
    
    
    /csv/stations/lastclick
    /csv/stations/lastclick/5
    
    
    
    /m3u/stations/lastclick
    /m3u/stations/lastclick/5
    
    
    
    /pls/stations/lastclick
    /pls/stations/lastclick/5
    

A list of stations that were clicked recently, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset  
`hidebroken` | `false` | `true`, `false` | do list/not list broken stations

 

## Stations by recently changed

> **Syntax:**
    
    
    /json/stations/lastchange
    /json/stations/lastchange/rowcount
    
    
    
    /xml/stations/lastchange
    /xml/stations/lastchange/rowcount
    
    
    
    /csv/stations/lastchange
    /csv/stations/lastchange/rowcount
    
    
    
    /m3u/stations/lastchange
    /m3u/stations/lastchange/rowcount
    
    
    
    /pls/stations/lastchange
    /pls/stations/lastchange/rowcount
    

> **Results:**
> 
> Array of struct '[station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations/lastchange
    /json/stations/lastchange/5
    
    
    
    /xml/stations/lastchange
    /xml/stations/lastchange/5
    
    
    
    /csv/stations/lastchange
    /csv/stations/lastchange/5
    
    
    
    /m3u/stations/lastchange
    /m3u/stations/lastchange/5
    
    
    
    /pls/stations/lastchange
    /pls/stations/lastchange/5
    

A list of stations that were added or changed recently, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset  
`hidebroken` | `false` | `true`, `false` | do list/not list broken stations

 

## Stations by votes

> **Syntax:**
    
    
    /json/stations/topvote
    /json/stations/topvote/rowcount
    
    
    
    /xml/stations/topvote
    /xml/stations/topvote/rowcount
    
    
    
    /csv/stations/topvote
    /csv/stations/topvote/rowcount
    
    
    
    /m3u/stations/topvote
    /m3u/stations/topvote/rowcount
    
    
    
    /pls/stations/topvote
    /pls/stations/topvote/rowcount
    

> **Results:**
> 
> Array of struct '[station](https://docs.radio-browser.info/#station)'
> 
> **Example:**
    
    
    /json/stations/topvote
    /json/stations/topvote/5
    
    
    
    /xml/stations/topvote
    /xml/stations/topvote/5
    
    
    
    /csv/stations/topvote
    /csv/stations/topvote/5
    
    
    
    /m3u/stations/topvote
    /m3u/stations/topvote/5
    
    
    
    /pls/stations/topvote
    /pls/stations/topvote/5
    

A list of the highest-voted stations. You can add a parameter with the number of wanted stations, supported output formats: JSON, XML, CSV, M3U, PLS, XSPF, TTL

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`offset` | `0` | `0`,`1`,`2`,`3`,... | starting value of the result list from the database. For example, if you want to do paging on the server side.  
`limit` | `100000` | `0`,`1`,`2`,`3`,... | number of returned datarows (stations) starting with offset  
`hidebroken` | `false` | `true`, `false` | do list/not list broken stations

 

## Old versions of stations

> **Syntax:**
    
    
    /json/stations/changed
    /json/stations/changed/stationuuid
    
    
    
    /xml/stations/changed
    /xml/stations/changed/stationuuid
    
    
    
    /csv/stations/changed
    /csv/stations/changed/stationuuid
    

> **Example:**
    
    
    /json/stations/changed?lastchangeuuid=123&limit=10
    /json/stations/changed/123
    
    
    
    /xml/stations/changed?lastchangeuuid=123&limit=10
    /xml/stations/changed/123
    
    
    
    /csv/stations/changed?lastchangeuuid=123&limit=10
    /csv/stations/changed/123
    

A list of old versions of stations from the last 30 days, and you can also retrieve the history of a single station by its ID. They are not visible through any other API calls. Station ID can be an ID or a station UUID, supported output formats: JSON, XML, CSV

### Parameters:



Name | Default value | Possible value | Description  
---|---|---|---  
`lastchangeuuid` |  | valid UUID | If defined, only show changes that happened after the one with this UUID. Is ignored if uuids is set.  
`limit` | `999999` | `0`,`1`,`2`,`3`,... | number of returned datarows (changes)

 

[json](https://docs.radio-browser.info/) [xml](https://docs.radio-browser.info/) [csv](https://docs.radio-browser.info/) [m3u](https://docs.radio-browser.info/) [pls](https://docs.radio-browser.info/) [xspf](https://docs.radio-browser.info/)
