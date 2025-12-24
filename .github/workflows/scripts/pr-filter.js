export default async ({ github, context, core }) => {
  const pr = context.payload.pull_request;
  const body = pr.body === null ? '' : pr.body;

  // Remove HTML comments robustly: apply replacement until stable
  function removeHtmlComments(input) {
    const pattern = /<!--[\s\S]*?-->/g;
    let previous;
    let current = input;
    do {
      previous = current;
      current = current.replace(pattern, '');
    } while (current !== previous);
    return current;
  }

  const markdown = removeHtmlComments(body);

  const action = context.payload.action;

  const isValid = true; // placeholder - preserve existing logic here

  // TODO: implement the rest of the script logic as needed
  return { markdown, action, isValid };
};
