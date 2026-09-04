# Fix — images and files will not display

Attachments upload correctly and reach Google Drive. They cannot be read back.
Clicking one returns `{"error":"Missing auth token"}` and thumbnails are broken
images.

---

## The cause, reproduced against the published deployment

I called the endpoint directly, from outside the browser:

| Request | Result |
|---|---|
| `GET /files/z9700ye0dvnappank3re24s53x8dr7gs` with no credential | **HTTP 401 `{"error":"Missing auth token"}`** |
| Same with `Authorization: Bearer <a token>` | HTTP 403 `{"error":"Forbidden"}` |
| Same with `?token=<a token>` | HTTP 403 `{"error":"Forbidden"}` |

The first line is exactly the error being reported, and exactly what a browser
sends for an `<img>` tag: a plain GET with no `Authorization` header.

The 403s matter too. They prove the endpoint is reachable and its authentication
check works — it correctly distinguishes no credential from a wrong one. **Nothing
is wrong with `serveFile`, with the Drive connection, or with the files.** Ten
images reached Drive today in the correct folders under their file identifiers,
and two of them download and decode as valid images.

The single defect is `src/pages/messages/_components/ThreadPanel.tsx` line 201:

```ts
const servingUrl = convexSiteUrl ? `${convexSiteUrl}/files/${fileId}` : null;
```

That URL carries no credential, and an `<img>` element cannot add one. It has no
way to set a header.

## The fix

Fetch the bytes in JavaScript with the credential attached, turn the response
into an object URL, and use that as the image source. The comment at line 187
already says this is what the component is supposed to do — *"Fetches bytes
through the platform's /files/:fileId endpoint"* — it just never got written.

```ts
const res = await fetch(`${convexSiteUrl}/files/${fileId}`, {
  headers: { Authorization: `Bearer ${token}` },
});
if (!res.ok) { /* show a broken-file state with the status code, not a silent gap */ }
const objectUrl = URL.createObjectURL(await res.blob());
// <img src={objectUrl} />
// URL.revokeObjectURL(objectUrl) on unmount
```

Apply it to every place a stored file is displayed — the thumbnail, the full-size
view, and the download link — in `ThreadPanel` and in `ChannelPanel`. Revoke each
object URL when its component unmounts, or the browser leaks memory as a person
scrolls a long conversation.

## Do not use the query parameter

`serveFile` accepts `?token=` and appending it to the image source is the tempting
one-character fix. **Do not.** The value is the OIDC `tokenIdentifier` — a
long-lived identity, not a short-lived session key. In an image source it lands in
browser history, in the `Referer` header of any outbound link, and in any
screenshot of the address bar. A leaked one is a working credential for that
person's account.

## Show a real failure state

When the fetch fails, render a visible broken-file state carrying the HTTP status.
A thumbnail that silently renders nothing is why this took a day to find. A person
should be able to read the failure off the screen and repeat it to us.

## Prove it

Do not report this fixed on a clean build. Do all four and report what you saw:

1. Open a photograph in a space. Does the thumbnail render?
2. Click it. Does the full-size image open?
3. Do the same in a record thread under THREADS.
4. Open a non-image attachment — the PDF `Section V.8 - LRMC Ph 2 - RFP_Signed
   5.25.pdf` on project PRJ-2026-0004. Does it download and open?

Then publish, and give me the published URL.
