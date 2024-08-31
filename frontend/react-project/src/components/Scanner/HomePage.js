import React from "react";

export default function HomePage(props) {
	const { file, setFile } = props;

	return (
		<main className="flex-1 p-4 flex flex-col gap-3 text-center sm:gap-4 md:gap-5 justify-center pb-20">
			<h1 className="font-semibold text-5xl sm:text-6xl md:text-7xl">
				Scammer <span className="text-blue-400 bold">Scanner</span>
			</h1>
			<h3 className="font-medium md:text-lg">
				Capture <span className="text-blue-400">&rarr;</span> Upload{" "}
				<span className="text-blue-400">&rarr;</span> Detect
			</h3>
			<label className="flex specialBtn px-4 py-2 rounded-xl items-center text-base justify-between gap-4 mx-auto w-72 max-w-full my-4 cursor-pointer">
				<input
					onChange={(e) => {
						const tempFile = e.target.files[0];
						setFile(tempFile);
					}}
					className="hidden"
					type="file"
					accept=".pdf, .png"
				></input>
				<p className="text-blue-400">Detect Now</p>
				<i className="fa-regular fa-image"></i>
			</label>
			<p className="italic text-slate-400">Protect Yourself Today</p>
		</main>
	);
}
