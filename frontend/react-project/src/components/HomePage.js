import React from "react";

export default function HomePage(props) {
	const { setAudioStream, setFile } = props;

	return (
		<main className="flex-1 p-4 flex flex-col gap-3 text-center sm:gap-4 md:gap-5 justify-center pb-20">
			<h1 className="font-semibold text-5xl sm:text-6xl md:text-7xl">
                Scammer<span className="text-blue-400 font-bold">Scanner</span>
            </h1>

			<h3 className="font-medium md:text-lg">
				Upload a screenshot to check if it's a scam!
			</h3>   
			
			<p className="text-base">
				{" "}
				<label className="text-blue-400 cursor-pointer hover:text-blue-600 duration-200">
					Upload{" "}
					<input
						onChange={(e) => {
							const tempFile = e.target.files[0];
							setFile(tempFile);
						}}
						className="hidden"
						type="file"
						accept=".png"
					></input>
				</label>{" "}
				a png file
			</p>
		</main>
	);
}
