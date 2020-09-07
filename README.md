# "Accept All": The Landscape of Cookie Banners in Greece & the UK
Hello, there! Welcome to the Github page of my [MSc Cyber Security](https://www.york.ac.uk/study/postgraduate-taught/courses/msc-cyber-security/) project. This is a study about Cookie Banners, and the privacy options that they provide, in Greece and the UK. By extending [OpenWPM](https://github.com/mozilla/OpenWPM), we were able to scrape over 14k websites and collect 8k Cookie Banners. 

![](https://media.giphy.com/media/2wZVM6cABptwvoZ4Gx/giphy.gif)

## Tools & Methods
In order to crawl that many websites and collect their Cookie Notices, this project developed a set of novel methods and extended existing ones. For instance, in order to identify the most pupolar websites in Greece and the UK, a number of different tools were built to parse the [Tranco](https://tranco-list.eu) and verify that the extracted websites allow crawling by checking their robots.txt and Terms of Service pages. 

Moreover, OpenWPM, a popular web privacy measurement framework, was extended so that it identifies Cookie Banners with the aid of the ["I don't care about cookies list"](https://www.i-dont-care-about-cookies.eu).

You can find all the code and how to run it under the [`code`](https://github.com/george-kampanos/i-like-cookies/tree/master/code) directory of this Git page. Why not give it a go in websites of your country? :) 

## Results
Overall, this survey identified issues with GDPR (and Data Privacy Act 2018 for the UK) compliance across Greece and the UK. For instance, while we found Cookie Banners in over 50% of our dataset, there was an average of 12% of websites that did not display a Cookie Notice even though they used Third-Party Cookies for tracking (see below figure).

![](https://github.com/george-kampanos/i-like-cookies/blob/master/paper/example_data/fig1.png)

Furthermore, we found evidence that websites nudge users towards privacy intrusive options through the privacy options that they provide in their Cookie Banners. For example, almost all Cookie Banners displayed an "Accept" button (depicted in the next Figure).

![](https://github.com/george-kampanos/i-like-cookies/blob/master/paper/example_data/fig2.png)

You can see the full set of results in the [`data`](https://github.com/george-kampanos/i-like-cookies/tree/master/data) directory of this Github. 

## The paper
You can download and read the full paper [here](https://github.com/george-kampanos/i-like-cookies). It discusses in detail all the code and methods that were mentioned here. 

Hope you've enjoyed my MSc Project! Drop me a line if you repeated the study for your country (or just want to say hi) [here](https://uk.linkedin.com/in/kampanosg). 

![](https://media.giphy.com/media/syBlSgDbjsMHC/giphy.gif)