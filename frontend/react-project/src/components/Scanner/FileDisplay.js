import React,{ Component } from "react";

export default function FileDisplay(props) {
	const url = "/upload";
	const { handleFileReset, file } = props;

	const handleFileUpload = async () => {
		if (!file) {
			alert("No file selected");
			return;
		}

		const formData = new FormData();
		formData.append("file", file);

		try {
			const response = await fetch(url, {
				method: "POST",
				body: formData,
			});

			if (!response.ok) {
				throw new Error("File upload failed");
			}
		} catch (error) {
			console.error("Error uploading file: ", error);
			alert("Error uploading file");
		}
	};

	return (
		<main className="flex-1 p-4 flex flex-col gap-3 text-center sm:gap-4 md:gap-5 justify-center pb-20 w-fit max-w-full mx-auto">
			<h1 className="font-semibold text-4xl sm:text-5xl md:text-6xl">
				Your <span className="text-blue-400 bold">File</span>
			</h1>
			<div className="mx-auto flex flex-col text-left mb-4 my-4">
				<h3 className="font-semibold">Name</h3>
				<p>{file.name}</p>
			</div>
			<div className="flex items-center justify-between gap-4">
				<button
					onClick={handleFileReset}
					className="text-slate-400 hover:text-blue-600 duration-200"
				>
					Reset
				</button>
				<button
					onClick={handleFileUpload}
					className="specialBtn px-3 p-2 rounded-lg text-blue-400 flex items-center gap-2 font-medium"
				>
					<p>Detect</p>
					<i class="fa-solid fa-user-secret"></i>
				</button>
			</div>
		</main>
	);
}
