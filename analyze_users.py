import csv, operator, argparse
import config

users_file = config.users_file

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--option', required=False, default="top", action='store', help='Option')
	parser.add_argument('-n', '--number', required=False, default="5", action='store', help='Number')
	my_args = parser.parse_args()
	return my_args

def top(users_sorted, max_users):
	for user in reversed(users_sorted[(-max_users):]):
		print 'User:%s   \tValue:%s' % (user[0],user[1])


def lim(users_sorted, limit):
	for user in reversed(users_sorted):
		if user[1] > limit:
			print 'User:%s   \tValue:%s' % (user[0],user[1])
		else:
			break

def main():
	csvFile = open(users_file, 'rb')
	csvReader = csv.reader(csvFile)
	all_csv = [line for line in csvReader]
	users = {}
	for row in all_csv[1:]:
		if row[0] in users:
			users[row[0]] = int( users[row[0]] ) + int( row[1] )
		else:
			users[row[0]] = int(row[1])
	users_sorted = sorted(users.items(), key=lambda x: x[1] )
	args = get_args()
	if args.option == "top":
		top(users_sorted, int(args.number))
	else:
		lim(users_sorted, int(args.number))


if __name__ == "__main__":
    main()