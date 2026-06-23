export default async function handler(req, res) {
  const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
  const url = `${backendUrl}/api/datasets`

  try {
    const response = await fetch(url)
    const data = await response.json()

    if (!response.ok) {
      return res.status(response.status).json({ error: data.detail || "Failed to fetch datasets" })
    }

    return res.status(200).json(data)
  } catch (error) {
    return res.status(500).json({ error: error.message || "Unexpected error fetching datasets" })
  }
}
