## CVPartner scraper

This is a package for scraping the cvpartner api

### Getting started

Once this is in the package index:
`$ pip install cvpartnerpy`

#### Usage

The package has support for getting user metadata and CVs attached to users.
This can be used to scrape out all user CVs from the api:

```python

cvp = CVPartner(org='myorg', api_key=os.environ['CVPARTNER_API_KEY'])

with open('user.ndjson', 'w') as f:
  for u in cvp.get_users_from_api():
      user_id = u['user_id']
      cv_id = u['default_cv_id']
      user_cv = cvp.get_user_cv(user_id, cv_id)
      f.write(json.dumps(user_cv))
```
