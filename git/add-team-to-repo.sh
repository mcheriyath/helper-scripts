username=your_user
password=your_password

org=your_org
repo=your_repo

team=Developers

teamid=$(curl -s --user $username:$password "https://api.github.com/orgs/$org/teams" | \
    jq --arg team "$team" '.[] | select(.name==$team) | .id')

curl -v -H "Authorization: Token $TOKEN" -d "" -X PUT "https://api.github.com/teams/$teamid/repos/$org/$repo"
