let $container = $('#accordion');
let temp1 = () => {
    let j = 0;
    for (let i in obj1) {
        j++;
        let innerObj = obj1[i];
        let id = innerObj.id;
        let sh = innerObj.sh;
        const headingHTML = createHeadingHtml(i, id, sh, j);
        $container.append(headingHTML);
    }
}

let temp2 = (value) => {
    console.log(value);
    for (const subHeading in obj2) {
        if (subHeading === value) {
            $container.empty();
            let subPageHtml = `
            <div class="container">
			    <div class="alert alert-warning" role="alert">
				    ${subHeading}
		  	    </div>
		  	    <p class="">Generally Asked Questions related to this topic</p>
            </div>`;
            $container.append(subPageHtml);
            let i = 0;
            for (const Question in obj2[subHeading]) {
                    i++;
                    const Answer = obj2[subHeading][Question];
                    subPageHtml = createSubpage(obj2[subHeading], Question, Answer, i);
                    $container.append(subPageHtml);
            }
            break;
        }
    }
}

temp1();