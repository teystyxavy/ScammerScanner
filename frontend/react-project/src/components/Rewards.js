import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Rewards() {
	const [rewards, setRewards] = useState([]);
	const [userPoints, setUserPoints] = useState(0);
	const navigate = useNavigate();

	useEffect(() => {
		const isLogged = localStorage.getItem("isLogged");
		if (!isLogged) {
			navigate("/login");
		}
	}, [navigate]);

	useEffect(() => {
		const fetchUserData = async () => {
			try {
				const pointsResponse = await fetch("/api/user/points", {
					method: "GET",
					credentials: "include",
				});

				if (pointsResponse.ok) {
					const pointsData = await pointsResponse.json();
					setUserPoints(pointsData.points || 0);
				} else {
					console.error("Failed to fetch user points");
				}

				const rewardsResponse = await fetch("/api/rewards");
				if (rewardsResponse.ok) {
					const rewardsData = await rewardsResponse.json();
					setRewards(rewardsData);
				} else {
					console.error("Failed to fetch rewards");
				}
			} catch (error) {
				console.error("Error fetching user data or rewards:", error);
			}
		};

		fetchUserData();
	}, []);

	const handleRedeem = async (reward_id) => {
		const updatedRewards = rewards.map((reward) =>
			reward.reward_id === reward_id ? { ...reward, isRedeeming: true } : reward
		);
		setRewards(updatedRewards);

		try {
			const response = await fetch("/api/claim_reward", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ reward_id }),
				credentials: "include",
			});

			if (response.ok) {
				const data = await response.json();
				alert(data.message);

				const updatedUserPoints =
					userPoints -
					rewards.find((reward) => reward.reward_id === reward_id)
						.points_required;
				setUserPoints(updatedUserPoints);

				setRewards((rewards) =>
					rewards.filter((reward) => reward.reward_id !== reward_id)
				);
			} else {
				const errorData = await response.json();
				alert(errorData.error || "Failed to claim the reward.");
			}
		} catch (error) {
			alert("Something went wrong while claiming the reward.");
		} finally {
			const resetRewards = rewards.map((reward) =>
				reward.reward_id === reward_id
					? { ...reward, isRedeeming: false }
					: reward
			);
			setRewards(resetRewards);
		}
	};

	const containerStyle = {
		padding: "40px 20px",
		minHeight: "100vh",
	};

	const headerStyle = {
		display: "flex",
		justifyContent: "space-between",
		alignItems: "center",
		marginBottom: "40px",
	};

	const headingStyle = {
		fontSize: "32px",
		fontWeight: "bold",
		color: "#333",
	};

	const pointsStyle = {
		fontSize: "20px",
		fontWeight: "bold",
		color: "#555",
	};

	const gridStyle = {
		display: "grid",
		gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
		gap: "20px",
	};

	const cardStyle = {
		backgroundColor: "#ffffff",
		borderRadius: "10px",
		overflow: "hidden",
		boxShadow: "0 10px 20px rgba(0, 0, 0, 0.1)",
		textAlign: "center",
		padding: "20px",
		position: "relative",
	};

	const imageStyle = {
		width: "100%",
		height: "150px",
		objectFit: "contain",
	};

	const categoryStyle = {
		fontSize: "14px",
		color: "#888",
		marginTop: "10px",
	};

	const nameStyle = {
		fontSize: "18px",
		fontWeight: "bold",
		marginTop: "10px",
	};

	const pointsRequiredStyle = {
		fontSize: "24px",
		fontWeight: "bold",
		color: "#333",
		marginTop: "10px",
	};

	const redeemButtonStyle = {
		backgroundColor: "#00aaff",
		color: "#fff",
		border: "none",
		borderRadius: "20px",
		padding: "10px 20px",
		marginTop: "20px",
		cursor: "pointer",
	};

	const lockedButtonStyle = {
		...redeemButtonStyle,
		backgroundColor: "#999",
		cursor: "not-allowed",
	};

	return (
		<div style={containerStyle}>
			<div style={headerStyle}>
				<h1 style={headingStyle}>My Rewards</h1>
				<div style={pointsStyle}>Points: {userPoints}</div>
			</div>
			<div style={gridStyle}>
				{rewards.map((reward) => (
					<div key={reward.reward_id} style={cardStyle}>
						<img
							src={reward.image_url}
							alt={reward.reward_name}
							style={imageStyle}
						/>
						<div style={categoryStyle}>{reward.category}</div>
						<div style={nameStyle}>{reward.reward_name}</div>
						<div style={pointsRequiredStyle}>{reward.points_required} pts</div>
						{userPoints >= reward.points_required ? (
							<button
								style={redeemButtonStyle}
								onClick={() => handleRedeem(reward.reward_id)}
								disabled={reward.isRedeeming}
							>
								{reward.isRedeeming ? "Processing..." : "Redeem now"}
							</button>
						) : (
							<button style={lockedButtonStyle} disabled>
								Not enough points
							</button>
						)}
					</div>
				))}
			</div>
		</div>
	);
}

export default Rewards;
