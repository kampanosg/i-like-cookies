<h1>"Accept All": The Landscape of Cookie Banners in Greece & the UK</h1>
<p>Hello, there! Welcome to the Github page of my <a href="https://www.york.ac.uk/study/postgraduate-taught/courses/msc-cyber-security/" target="_blank">MSc Cyber Security</a> project. This is a study about Cookie Banners, and the privacy options that they provide, in Greece and the UK. By extending <a href="https://github.com/mozilla/OpenWPM" target="_blank">OpenWPM</a>, we were able to scrape over 14k websites and collect 8k Cookie Banners.</p>

<p align="center">
<img src="https://media.giphy.com/media/2wZVM6cABptwvoZ4Gx/giphy.gif" />
</p>

<h2>Tools & Methods</h2>
<p>In order to crawl that many websites and collect their Cookie Notices, this project developed a set of novel methods and extended existing ones. For instance, in order to identify the most pupolar websites in Greece and the UK, a number of different tools were built to parse the <a href="https://tranco-list.eu" target="_blank">Tranco</a> and verify that the extracted websites allow crawling by checking their robots.txt and Terms of Service pages.</p>

<p>Moreover, OpenWPM, a popular web privacy measurement framework, was extended so that it identifies Cookie Banners with the aid of the <a href="https://www.i-dont-care-about-cookies.eu" target="_blank">I don't care about cookies list</a>.</p>

<p>You can find all the code and how to run it under the <a href="https://github.com/george-kampanos/i-like-cookies/tree/master/code" target="_blank">code</a> directory of this Git page. Why not give it a go in websites of your country? :) </p>

<h2>The Paper</h2>
Our researchers has been accepted to and to appear in the proceedings of IFIP SEC 2021! You can read it by... 

1. Downloading it directly from <a href="#" target="_blank">arXiv</a>
2. Pulling it from our GitHub <a href="https://github.com/kampanosg/i-like-cookies/blob/master/paper/main.pdf" target="_blank">repo</a>
3. Building it from source as shown below (<a href="https://www.latex-project.org/get/" target="_blank">Latex</a> is required)


```sh
# fork the repo
cd paper
./build.sh
```

<h2>Findings</h2>

<h3>Cookie Banners are not everywhere</h3>
<p>Our  findings  show  that  almost half of the websites we surveyed display a cookie banner. More specifically,around 48% of Greek and 44% of the UK websites included a cookie notice.</p>
<p align="center">
<img src="https://github.com/kampanosg/i-like-cookies/blob/master/paper/example_data/fig1.png?raw=true" />
</p>

<h3>Direct opt-outs are rare</h3>
<p>The most prevalent number of options in both countries is two. The mean numberof options is 2.1 for Greece and 1.8 for the UK. Worryingly,  a  considerable  proportion  of  cookie banners provide either no option or only one option to the user. As the figure below shows, althoughAffirmative  options  are  quite  ubiquitous  in  cookie  banners  in  both  countries(Greece:  95%,  UK:  88%),  Negative  options  are  quite  rare  (Greece:  20%,  UK:6%)</p>

<p align="center">
<img src="https://github.com/kampanosg/i-like-cookies/blob/master/paper/example_data/fig2.png?raw=true" />
</p>

<h3>Websites wants you to trust Cookie Banners</h3>
<p>To  get  a  more  comprehensive  view  of  the  connotations  relayed  by  cookiebanner texts in the UK, we performed an automated sentiment analysis of thewords used in all UK banner texts using <a href="https://github.com/metalcorebear/NRCLex" target="_blank">NRCLex</a>. The analysis found that agenerally positive emotional affect was present in around 80% of the banner texts,whereas a generally negative affect was present in only around 14%. Besides, anoverwhelming majority (of more than 9 in 10) of the texts with a negative affectalso  had  a  positive  effect  present  as  well.  Looking  at  more  specific  emotionalaffects, trust and joy are among the most prevalent, present in around 66% and46% of the texts, respectively. The prevalence of general and specific emotionalaffects is shown in the figure below.</p>

<p align="center">
<img src="https://github.com/kampanosg/i-like-cookies/blob/master/paper/example_data/fig3.png?raw=true" />
</p>

<h2>Reference</h2>
<p>Please cite the following paper if you use this repository:</p>
<blockquote>George Kampanos and Siamak F. Shahandashti. "Accept All: The Landscape of Cookie Banners in Greece and the UK". To appear in the proceedings of the 36th International Conference on ICT Systems Security and Privacy Protection (IFIP SEC 2021)</blockquote>


<h2>That's it!</h2>
Hope you've enjoyed my MSc Project! Drop me a line if you repeated the study for your country (or just want to say hi) <a href="https://uk.linkedin.com/in/kampanosg" target="_blank">here</a>. 

<p align="center">
  <img src="https://media.giphy.com/media/syBlSgDbjsMHC/giphy.gif" />
</p>
