const createSubHeadingHtml = (sh) => {
    let subHeadingHtml = ``;
    for (const subHeading in sh) {
        if (sh.hasOwnProperty(subHeading)) {
            const link = sh[subHeading];
            subHeadingHtml += `<a href="#" onClick="temp2(this.innerText)" class="list-group-item list-group-item-action">${subHeading}</a>`;
        }
    }
    return subHeadingHtml;
}
                                        
const createHeadingHtml = (h, id, sh, j) => {
    let subHeadingHtml = createSubHeadingHtml(sh);
    return `
            <div class="panel">
				<div class="panel-header" id="${id}">
					<button class="panel-link " data-toggle="collapse" data-target="#collapse${j}" aria-expanded="false" aria-controls="collapse${j}">${h}</button>
				</div>
				<div id="collapse${j}" class="collapse" aria-labelledby="${id}" data-parent="#accordion">
					<div class="panel-body">
						<div class="row">
							<div class="col-sm-10 offset-sm-1">
								<div class="row">
									<div class="list-group list-group-flush col-12 pr-0">
										${subHeadingHtml}
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
    `;
}

const createSubpage = (subHeading, Question, Answer, i) => {
	return `
	<div>
		<p class="mt-3">
			<a class="btn" data-toggle="collapse" href="#collapse${i}" role="button" aria-expanded="false" aria-controls="collapse${i}">
				Q.
			</a>
			<a class="" data-toggle="collapse" href="#collapse${i}" role="button" aria-expanded="false" aria-controls="collapse${i}">
				${Question}
			</a>
		</p>
		<div class="collapse" id="collapse${i}">
			<div class="card card-body">
				<p class="">${Answer}</p>
				<div class="card  bg-light mb-3" >
					<div class="card-header">Are you satisfied with answer?</div>
					<div class="card-body" >
						<div class="card-title">
							<button type="button" onclick="successfully()" class="btn text-success btn-outline-dark">Yes</button>
							<button type="button" onclick="failure()" class="btn text-danger btn-outline-dark">No</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	`
}