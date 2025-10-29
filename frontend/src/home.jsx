
function BlogPost({title,body,username,full=false}){
	let blogstyle = {
		border: "1px solid #333",
		padding: "10px"
	}
	
	let fullblogstyle = {
		fontSize: "14pt",
		width: "100vw",
		borderBottom: "1px solid #333",
		
		
	}
	
	let userstyle = {
		color: "#777",
		fontSize: "8pt",
		fontWeight: "400"
	}
	return (
	<div style={(!full) ? blogstyle: fullblogstyle}>
	<h5 stylle={userstyle}>{username}</h5>
	<h3>{title}</h3>
	<p>{body.slice(0,50)}...</p>
	</div>
	)
}

function BlogList({list}){
	let bloglinkstyle = {
		color: "#333",
		
	}
	
	let blogs = list.map((l) => (<a style={bloglinkstyle} href={"blog/" + (l.id-1)}><BlogPost title={l.title} body={l.body} username={l.username} /></a>))
	return (
	<>
	{blogs}
	</>
	)
	
}

function Navbar(){
	let navbarstyle = {
		position: "fixed",
		top: '0',
		
		background: "#cdcdcd",
		display: "flex",
		justifyContent: "space-between",
		alignItems: "center",
		width: "100vw"
		
	}
	return (
	<div style={navbarstyle}>
	<a href="home">Home </a>
	<a href="new">New</a>
	<a href="login">Login</a>
	</div>
	)
}
//This is the homepage here is where all your main components goto
export default function Home(){
	let mockdata = [{
		"id":1,
		"username":"Hawk",
		"title": "Hello I am Hawk",
		"body":"Nice to meet yall"
	},{
		"id":2,
		"username":"Hockey",
		"title": "Hello I am Hockey",
		"body":"Nice to meet yall"
	},{
		"id":3,
		"username":"Dragabar",
		"title": "Hella bitches",
		"body":"Nice to fuck yall"
	},{
		"id":4,
		"username":"Ha",
		"title": "Hahahahahahahahha",
		"body":"hahahahahhahahahhahahahahahahahahhahaha?不?不?不?不?不?不?不"
	}]
	
	if (window.location.pathname === "/")
	{
		let homestyle = {
			justifyContent: "center"
		}
		
		return (
		<div style={homestyle}>
	    <Navbar />
		<h1>Blog Posts</h1>
		<BlogList list={mockdata}/>
		</div>
		)
	}
	else{
		let route = window.location.pathname
		route = route.split("/")
		console.log(route)
		
		if (route[1] === "blog"){
			let post = mockdata[route[2]]
			return (
			<BlogPost username={post.username} title={post.title} body={post.body} full={true}/>
			)
		}
	}
}