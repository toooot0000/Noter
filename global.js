const urgencyLevel = ["不急", "有点急", "很急", "不完成能死"];

const objToStyle = function (obj) {
	let res = "";
	for (props in obj) {
		res += props + ":" + obj[props] + ";";
	}
	return res;
};

export default {
	urgencyLevel,
	objToStyle,
};
