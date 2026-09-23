export default async function handler(request) {
  console.log("linkblog request received");
  console.log(await request.text());

  return Response.json({
    ok: true,
    title: "Test"
  });
}

export const config = {
  path: "/api/linkblog",
};
