# Magazine Downloader 

This is a small Python experiment I built out of curiosity.  
I came across a site that exposed its images directly in the browser’s developer tools.  
I tried automating the process of grabbing those images and stitching them into a single PDF.  

---

So, pasting this link in the console gets me all the images:

```js
const imgs2 = document.querySelectorAll('img[highreslist]'); 
const links2 = Array.from(imgs2) 
  .map(img => img.getAttribute('highreslist')) 
  .filter(Boolean); 
 
if (!links2.length) {
  console.warn('No pages found. Scroll the thumbnail list fully, then run again.'); 
} else {
  console.log(`Found ${links2.length} pages`);
  
  // Add current date to filename for organization
  const currentDate = new Date();
  const monthYear = currentDate.toLocaleDateString('en-US', { year: 'numeric', month: '2-digit' });
  const filename = `links_${monthYear.replace('/', '_')}.txt`;
  
  const blob2 = new Blob([links2.join('\n')], { type: 'text/plain' }); 
  const downloadLink = document.createElement('a'); 
  downloadLink.href = URL.createObjectURL(blob2); 
  downloadLink.download = filename;
  downloadLink.click(); 
}
```

This downloads all the image links into a .txt file.
Make sure the .txt file and the Python script are in the same folder.

Then run:

```bash
python make_pdf.py
```
This will take some time to download all the images in the folder and convert them into a PDF using requests and Pillow/img2pdf libraries.

I used it on a set of magazines that were freely exposed online.
I’m not going to mention the magazine’s name here
