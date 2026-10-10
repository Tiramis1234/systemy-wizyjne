// Thin wrapper around the backend HTTP API. No image processing happens here.

// Throws an Error with the backend's "detail" message, so the UI can show it.
async function request(url, options = {}) {
  let response
  try {
    response = await fetch(url, options)
  } catch {
    throw new Error('Cannot reach the backend. Is it running?')
  }
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`
    try {
      const body = await response.json()
      if (typeof body.detail === 'string') detail = body.detail
      else if (body.detail) detail = JSON.stringify(body.detail)
    } catch {
      // Body was not JSON; keep the status text.
    }
    throw new Error(detail)
  }
  return response
}

async function postJson(url, body) {
  const response = await request(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return response.json()
}

export async function listSamples() {
  return (await request('/api/samples')).json()
}

export function loadImageFromPath(path) {
  return postJson('/api/image/load', { path })
}

export async function uploadImage(file) {
  const form = new FormData()
  form.append('file', file)
  return (await request('/api/image/upload', { method: 'POST', body: form })).json()
}

// Image URLs get a changing "v" parameter so the browser fetches the new image.
export function inputImageUrl(version) {
  return `/api/workspace/input?v=${version}`
}
