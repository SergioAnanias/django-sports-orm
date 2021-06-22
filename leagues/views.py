from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q, Count



from . import team_maker

def index(request):
	context = {
		#sport orm 1
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"womenleagues": League.objects.filter(name__contains="Women"),
		"hockeyleagues": League.objects.filter(name__contains="hockey"),
		"allbutfootball": League.objects.exclude(sport="Football"),
		"conferenceleagues": League.objects.filter(name__contains="conference"),
		"atlanticleagues": League.objects.filter(name__contains="Atlantic"),

		"dallasteams": Team.objects.filter(location="Dallas"),
		"raptorteams": Team.objects.filter(team_name="Raptors"),
		"cityteams": Team.objects.filter(location__contains="City"),
		"teamstartwitht": Team.objects.filter(team_name__startswith="T"),
		"abcteams": Team.objects.order_by('location'),
		"reverseteams": Team.objects.order_by('-team_name'),

		"cooperplayers": Player.objects.filter(last_name='Cooper'),
		"joshuaplayers": Player.objects.filter(first_name='Joshua'),
		"cooperbutjoshua": Player.objects.filter(last_name='Cooper').exclude(first_name='Joshua'),
		"alexowyatt": Player.objects.filter(Q(first_name='Alexander') | Q(first_name='Wyatt')),
	
		# sports orm 2
		"atlanticteams": Team.objects.filter(league = League.objects.get(name="Atlantic Soccer Conference")),
		"penguinsplayers": Player.objects.filter(curr_team= Team.objects.get(team_name="Penguins")),
		"internationalbaseplayers": Player.objects.filter(curr_team__league__name="International Collegiate Baseball Conference"),
		"lopezplayers": Player.objects.filter(Q(curr_team__league__name="American Conference of Amateur Football") & Q(last_name="Lopez")),
		"footballplayers": Player.objects.filter(curr_team__league__sport="Football"),
		"sophiateams": Team.objects.filter(curr_players__first_name="Sophia"),
		"sophialeagues": League.objects.filter(teams__curr_players__first_name="Sophia"),
		"floresnotinwr": Player.objects.filter(last_name="Flores").exclude(curr_team__team_name="Roughriders", curr_team__location="Washington"),
		"samuelevansteams": Team.objects.filter(all_players__first_name="Samuel"),
		"manitobatigerplayers": Player.objects.filter(all_teams__team_name="Tiger-Cats"),
		"notinvikingsrn": Player.objects.filter(all_teams__team_name="Vikings").exclude(curr_team__team_name="Vikings"),
		"jacobgraybefore": Team.objects.filter(Q(all_players__first_name="Jacob") & Q(all_players__last_name="Gray")).exclude(Q(curr_players__first_name="Jacob") & Q(curr_players__last_name="Gray")),
		"joshuafed": Player.objects.filter(Q(all_teams__league__name="Atlantic Federation of Amateur Baseball Players") & Q(first_name="Joshua")),
		"morethan12": Team.objects.annotate(Count('all_players')),
		"allplayers": Player.objects.annotate(Count('all_teams')).order_by('all_teams__count')
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")